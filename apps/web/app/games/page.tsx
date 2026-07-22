"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { API_URL, authHeaders } from "@/lib/api";

type Game = {
  id: string;
  matchup: string;
  starts_at: string;
  venue: string;
  status: string;
  probable_pitchers: {away: string; home: string};
  weather?: {
    temperature_f?: number;
    wind_speed_mph?: number;
    wind_direction?: string;
    precipitation_probability?: number;
    short_forecast?: string;
  };
  qualified_picks: number;
};

export default function GamesPage() {
  const [games, setGames] = useState<Game[]>([]);
  const [message, setMessage] = useState("Loading games...");

  useEffect(() => {
    fetch(`${API_URL}/api/v1/games`, {headers: authHeaders()})
      .then(async r => {
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail ?? "Unable to load games");
        setGames(data); setMessage("");
      })
      .catch(e => setMessage(e.message));
  }, []);

  return (
    <main className="section container">
      <div className="eyebrow">MLB intelligence</div>
      <h1 style={{fontSize:"58px", textAlign:"left", marginLeft:0}}>Game board</h1>
      <p className="section-lead">Schedule, probable pitchers, weather, and qualified model signals.</p>
      {message && <div className="card">{message}</div>}
      <div className="grid">
        {games.map(game => (
          <Link href={`/games/${game.id}`} className="card" key={game.id}>
            <div className="pick-top">
              <div>
                <div className="eyebrow">{new Date(game.starts_at).toLocaleString()}</div>
                <h3>{game.matchup}</h3>
                <div className="muted">{game.venue}</div>
              </div>
              <span className="badge">{game.qualified_picks} signals</span>
            </div>
            <div className="metrics">
              <div className="metric"><span className="muted">Away starter</span><strong style={{fontSize:"14px"}}>{game.probable_pitchers.away || "TBD"}</strong></div>
              <div className="metric"><span className="muted">Home starter</span><strong style={{fontSize:"14px"}}>{game.probable_pitchers.home || "TBD"}</strong></div>
              <div className="metric"><span className="muted">Weather</span><strong style={{fontSize:"14px"}}>{game.weather?.short_forecast || "Pending"}</strong></div>
              <div className="metric"><span className="muted">Temperature</span><strong>{game.weather?.temperature_f ? `${game.weather.temperature_f}°` : "—"}</strong></div>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
