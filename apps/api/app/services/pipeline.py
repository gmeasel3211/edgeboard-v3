from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timezone
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import (
    Game, OddsSnapshot, Pick, PitcherSnapshot, RefreshRun,
    TeamSnapshot, WeatherSnapshot
)
from app.services.mlb_client import MLBStatsClient
from app.services.model_engine import (
    american_to_implied, evaluate_moneyline, no_vig_probabilities,
    projected_home_probability
)
from app.services.odds_client import OddsClient
from app.services.stadiums import STADIUMS
from app.services.weather_client import NWSClient, parse_wind_speed


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def to_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class RefreshPipeline:
    def __init__(self):
        self.odds = OddsClient()
        self.mlb = MLBStatsClient()
        self.weather = NWSClient()

    async def run_full(self) -> dict:
        result = {}
        result["mlb"] = await self.refresh_mlb()
        result["odds"] = await self.refresh_odds()
        result["weather"] = await self.refresh_weather()
        result["model"] = self.rebuild_card()
        return result

    async def refresh_mlb(self) -> dict:
        run_id = self._start_run("mlb")
        try:
            season = date.today().year
            schedule, standings = await self.mlb.schedule(), await self.mlb.standings(season)
            pitcher_ids: dict[int, str] = {}
            with SessionLocal() as db:
                for payload in schedule:
                    teams = payload.get("teams", {})
                    home = teams.get("home", {}).get("team", {})
                    away = teams.get("away", {}).get("team", {})
                    venue = payload.get("venue", {})
                    game_pk = payload.get("gamePk")
                    external_id = f"mlb-{game_pk}"
                    game = db.scalar(select(Game).where(Game.external_id == external_id)) or Game(external_id=external_id)
                    game.mlb_game_pk = game_pk
                    game.home_team = home.get("name", "")
                    game.away_team = away.get("name", "")
                    game.home_team_id = home.get("id")
                    game.away_team_id = away.get("id")
                    game.venue_name = venue.get("name", "")
                    game.venue_id = venue.get("id")
                    game.starts_at = parse_dt(payload.get("gameDate")) or datetime.now(timezone.utc)
                    game.status = payload.get("status", {}).get("detailedState", "scheduled")
                    home_pitcher = teams.get("home", {}).get("probablePitcher", {})
                    away_pitcher = teams.get("away", {}).get("probablePitcher", {})
                    game.home_probable_pitcher_id = home_pitcher.get("id")
                    game.home_probable_pitcher = home_pitcher.get("fullName", "")
                    game.away_probable_pitcher_id = away_pitcher.get("id")
                    game.away_probable_pitcher = away_pitcher.get("fullName", "")
                    if game.home_probable_pitcher_id:
                        pitcher_ids[game.home_probable_pitcher_id] = game.home_probable_pitcher
                    if game.away_probable_pitcher_id:
                        pitcher_ids[game.away_probable_pitcher_id] = game.away_probable_pitcher
                    game.home_score = teams.get("home", {}).get("score")
                    game.away_score = teams.get("away", {}).get("score")
                    game.source_updated_at = datetime.now(timezone.utc)
                    db.add(game)

                captured = date.today().isoformat()
                for record in standings:
                    team = record.get("team", {})
                    games_played = max(int(record.get("gamesPlayed", 0) or 0), 1)
                    runs_scored = int(record.get("runsScored", 0) or 0)
                    runs_allowed = int(record.get("runsAllowed", 0) or 0)
                    snap = db.scalar(select(TeamSnapshot).where(
                        TeamSnapshot.team_id == team.get("id"),
                        TeamSnapshot.season == season,
                        TeamSnapshot.captured_date == captured,
                    )) or TeamSnapshot(team_id=team.get("id"), season=season, captured_date=captured)
                    snap.team_name = team.get("name", "")
                    snap.wins = int(record.get("wins", 0) or 0)
                    snap.losses = int(record.get("losses", 0) or 0)
                    snap.runs_per_game = runs_scored / games_played
                    snap.runs_allowed_per_game = runs_allowed / games_played
                    snap.run_differential_per_game = (runs_scored - runs_allowed) / games_played
                    snap.raw = record
                    db.add(snap)
                db.commit()

            pitcher_count = 0
            for pitcher_id, name in pitcher_ids.items():
                stats = await self.mlb.pitcher_stats(pitcher_id, season)
                if not stats:
                    continue
                with SessionLocal() as db:
                    captured = date.today().isoformat()
                    snap = db.scalar(select(PitcherSnapshot).where(
                        PitcherSnapshot.pitcher_id == pitcher_id,
                        PitcherSnapshot.season == season,
                        PitcherSnapshot.captured_date == captured,
                    )) or PitcherSnapshot(
                        pitcher_id=pitcher_id, season=season, captured_date=captured
                    )
                    snap.pitcher_name = name
                    snap.era = to_float(stats.get("era"))
                    snap.whip = to_float(stats.get("whip"))
                    snap.strikeouts_per_9 = to_float(stats.get("strikeoutsPer9Inn"))
                    snap.walks_per_9 = to_float(stats.get("walksPer9Inn"))
                    snap.innings_pitched = to_float(stats.get("inningsPitched"))
                    snap.raw = stats
                    db.add(snap)
                    db.commit()
                    pitcher_count += 1
            details = {"games": len(schedule), "teams": len(standings), "pitchers": pitcher_count}
            self._finish_run(run_id, "success", details)
            return details
        except Exception as exc:
            self._finish_run(run_id, "failed", {}, str(exc))
            raise

    async def refresh_odds(self) -> dict:
        run_id = self._start_run("odds")
        try:
            events, usage = await self.odds.fetch_mlb_odds()
            rows = self.odds.normalize(events)
            with SessionLocal() as db:
                for event in events:
                    game = db.scalar(select(Game).where(Game.external_id == event["id"])) or Game(external_id=event["id"])
                    game.home_team = event["home_team"]
                    game.away_team = event["away_team"]
                    game.starts_at = parse_dt(event["commence_time"]) or datetime.now(timezone.utc)
                    game.status = "scheduled"
                    stadium = STADIUMS.get(game.home_team, {})
                    game.venue_name = stadium.get("venue", "")
                    db.add(game)
                for row in rows:
                    db.add(OddsSnapshot(
                        game_external_id=row["game_external_id"],
                        bookmaker=row["bookmaker"],
                        market=row["market"],
                        selection=row["selection"],
                        american_odds=row["american_odds"],
                        line=row["line"],
                        bookmaker_updated_at=parse_dt(row["bookmaker_updated_at"]),
                        captured_at=row["captured_at"],
                    ))
                db.commit()
            details = {"events": len(events), "outcomes": len(rows), "quota": usage}
            self._finish_run(run_id, "success", details)
            return details
        except Exception as exc:
            self._finish_run(run_id, "failed", {}, str(exc))
            raise

    async def refresh_weather(self) -> dict:
        run_id = self._start_run("weather")
        saved = 0
        try:
            with SessionLocal() as db:
                games = list(db.scalars(select(Game).where(Game.starts_at >= datetime.now(timezone.utc))).all())
            for game in games:
                stadium = STADIUMS.get(game.home_team)
                if not stadium or stadium.get("roof"):
                    continue
                periods = await self.weather.hourly_forecast(stadium["lat"], stadium["lon"])
                period = self.weather.closest_period(periods, game.starts_at)
                if not period:
                    continue
                with SessionLocal() as db:
                    db.add(WeatherSnapshot(
                        game_external_id=game.external_id,
                        forecast_time=parse_dt(period.get("startTime")),
                        temperature_f=to_float(period.get("temperature")),
                        wind_speed_mph=parse_wind_speed(period.get("windSpeed")),
                        wind_direction=period.get("windDirection", ""),
                        precipitation_probability=to_float(
                            (period.get("probabilityOfPrecipitation") or {}).get("value")
                        ),
                        short_forecast=period.get("shortForecast", ""),
                    ))
                    db.commit()
                    saved += 1
            details = {"forecasts": saved}
            self._finish_run(run_id, "success", details)
            return details
        except Exception as exc:
            self._finish_run(run_id, "failed", {}, str(exc))
            raise

    def rebuild_card(self) -> dict:
        with SessionLocal() as db:
            db.execute(delete(Pick).where(Pick.status == "pending"))
            games = list(db.scalars(select(Game).where(Game.starts_at >= datetime.now(timezone.utc))).all())
            created = 0
            for game in games:
                latest_time = db.scalar(select(OddsSnapshot.captured_at).where(
                    OddsSnapshot.game_external_id == game.external_id,
                    OddsSnapshot.market == "h2h",
                ).order_by(OddsSnapshot.captured_at.desc()).limit(1))
                if not latest_time:
                    continue
                odds = list(db.scalars(select(OddsSnapshot).where(
                    OddsSnapshot.game_external_id == game.external_id,
                    OddsSnapshot.market == "h2h",
                    OddsSnapshot.captured_at == latest_time,
                )).all())
                by_book = defaultdict(list)
                for odd in odds:
                    by_book[odd.bookmaker].append(odd)

                season, captured = date.today().year, date.today().isoformat()
                home_team = db.scalar(select(TeamSnapshot).where(
                    TeamSnapshot.team_id == game.home_team_id,
                    TeamSnapshot.season == season,
                    TeamSnapshot.captured_date == captured,
                )) if game.home_team_id else None
                away_team = db.scalar(select(TeamSnapshot).where(
                    TeamSnapshot.team_id == game.away_team_id,
                    TeamSnapshot.season == season,
                    TeamSnapshot.captured_date == captured,
                )) if game.away_team_id else None
                home_pitcher = db.scalar(select(PitcherSnapshot).where(
                    PitcherSnapshot.pitcher_id == game.home_probable_pitcher_id,
                    PitcherSnapshot.season == season,
                    PitcherSnapshot.captured_date == captured,
                )) if game.home_probable_pitcher_id else None
                away_pitcher = db.scalar(select(PitcherSnapshot).where(
                    PitcherSnapshot.pitcher_id == game.away_probable_pitcher_id,
                    PitcherSnapshot.season == season,
                    PitcherSnapshot.captured_date == captured,
                )) if game.away_probable_pitcher_id else None

                for bookmaker, outcomes in by_book.items():
                    home_outcome = next((x for x in outcomes if x.selection == game.home_team), None)
                    away_outcome = next((x for x in outcomes if x.selection == game.away_team), None)
                    if not home_outcome or not away_outcome:
                        continue
                    nv_home, nv_away = no_vig_probabilities(
                        [home_outcome.american_odds, away_outcome.american_odds]
                    )
                    home_model, factors = projected_home_probability(
                        home_team, away_team, home_pitcher, away_pitcher, nv_home
                    )
                    candidates = [
                        (home_outcome, home_model, nv_home),
                        (away_outcome, 1 - home_model, nv_away),
                    ]
                    for outcome, model_prob, market_prob in candidates:
                        metrics = evaluate_moneyline(
                            outcome.selection, outcome.american_odds, model_prob, market_prob
                        )
                        if metrics["edge_percent"] < 1.5 or metrics["expected_value_percent"] < 1.0:
                            continue
                        db.add(Pick(
                            sport="MLB",
                            game_id=game.external_id,
                            matchup=f"{game.away_team} @ {game.home_team}",
                            market="moneyline",
                            selection=outcome.selection,
                            sportsbook=bookmaker.title(),
                            american_odds=outcome.american_odds,
                            model_probability=model_prob,
                            market_probability=market_prob,
                            starts_at=game.starts_at,
                            status="pending",
                            explanation=(
                                f"Market-aware projection. Team rating difference {factors['team_diff']:+.2f}; "
                                f"starting-pitcher difference {factors['pitcher_diff']:+.2f}; "
                                "probabilities are blended with no-vig market consensus to reduce overconfidence."
                            ),
                            **metrics,
                        ))
                        created += 1
            db.commit()
        return {"picks": created}

    def _start_run(self, job_name: str) -> int:
        with SessionLocal() as db:
            run = RefreshRun(job_name=job_name, status="running")
            db.add(run)
            db.commit()
            db.refresh(run)
            return run.id

    def _finish_run(self, run_id: int, status: str, details: dict, error: str = "") -> None:
        with SessionLocal() as db:
            run = db.get(RefreshRun, run_id)
            if run:
                run.status = status
                run.details = details
                run.error_message = error
                run.finished_at = datetime.now(timezone.utc)
                db.commit()
