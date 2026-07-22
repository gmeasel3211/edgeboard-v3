import Link from "next/link";
import { Shell } from "@/components/shell";
import { MetricCard } from "@/components/metric-card";
import { PickCard } from "@/components/pick-card";
import { currentUser } from "@/lib/auth";
import { serverApi } from "@/lib/api";
import { localTime, pct, units } from "@/lib/format";
import type { Dashboard } from "@/lib/types";

export const metadata = { title: "Today's Board" };

export default async function DashboardPage() {
  const user = await currentUser();
  const data = await serverApi<Dashboard>("/dashboard/today");
  const paid = user?.role === "admin" || user?.tier === "pro" || user?.tier === "elite";
  const firstName = user?.display_name?.split(" ")[0] || "Bettor";

  return (
    <Shell>
      <section className="dashboardHero v35DashboardHero">
        <div>
          <span className="eyebrow">EDGEBOARD 3.5 · MLB COMMAND CENTER</span>
          <h1>Today’s betting board, {firstName}.</h1>
          <p>Last model render: {localTime(data.as_of)}. Prices are sourced only from FanDuel and DraftKings.</p>
        </div>
        <div className="dashboardStatus"><i /><span>MODEL ONLINE</span><b>{data.tier.toUpperCase()} ACCESS</b></div>
      </section>

      <section className="dashboardBody v35DashboardBody">
        <div className="boardSummary">
          <div><span>Official plays</span><strong>{data.official.length}</strong><small>Tracked recommendations</small></div>
          <div><span>Modeled games</span><strong>{data.games.length}</strong><small>Full slate coverage</small></div>
          <div><span>Watchlist</span><strong>{data.watchlist.length}</strong><small>Near-threshold prices</small></div>
          <div><span>Access</span><strong>{data.tier.toUpperCase()}</strong><small>{paid ? "Full card unlocked" : "Featured play only"}</small></div>
        </div>

        <div className="metricsGrid compact">
          <MetricCard label="Official record" value={`${data.record.wins}–${data.record.losses}–${data.record.pushes}`} note={`${data.record.pending} pending`} />
          <MetricCard label="Net units" value={units(data.record.units)} note={`${data.record.units_risked.toFixed(2)}u risked`} tone={data.record.units >= 0 ? "positiveTone" : "negativeTone"} />
          <MetricCard label="ROI" value={pct(data.record.roi)} note="Official plays only" />
          <MetricCard label="Average CLV" value={pct(data.record.average_clv)} note="Closing implied probability" />
        </div>

        {!paid && <div className="upgradeBanner v35Upgrade"><div><span className="eyebrow">FREE ACCESS</span><h2>You’re seeing the featured play.</h2><p>Unlock every official recommendation, full reasoning, risk analysis, game intelligence, and performance tracking.</p></div><Link className="button" href="/pricing">Unlock the full board</Link></div>}

        <section className="panel v35Panel">
          <div className="sectionHead"><div><span className="eyebrow">OFFICIAL CARD</span><h2>Today’s tracked plays</h2><p className="panelDescription">Every official recommendation is frozen at its listed book and price for transparent grading.</p></div><span>{data.official.length} visible</span></div>
          {data.official.length ? <div className="pickList">{data.official.map((pick) => <PickCard key={pick.id} pick={pick} locked={!paid} />)}</div> : <div className="emptyState"><strong>No official play yet.</strong><span>The model will not manufacture action when the available price fails to clear its thresholds.</span></div>}
        </section>

        {data.watchlist.length > 0 && paid && <section className="panel v35Panel"><div className="sectionHead"><div><span className="eyebrow">ELITE WATCHLIST</span><h2>Qualified bets below the official cutoff</h2><p className="panelDescription">Useful prices to monitor, but not part of the tracked official record.</p></div><span>{data.watchlist.length} candidates</span></div><div className="pickList">{data.watchlist.map((pick) => <PickCard key={pick.id} pick={pick} />)}</div></section>}

        <section className="panel v35Panel">
          <div className="sectionHead"><div><span className="eyebrow">GAME BOARD</span><h2>Every modeled matchup</h2><p className="panelDescription">Open a matchup for projected scoring, pitching context, weather, market pricing, and model signals.</p></div><span>{data.games.length} games</span></div>
          <div className="gameGrid v35GameGrid">
            {data.games.map((game) => <Link className="gameCard v35GameCard" href={paid ? `/game/${encodeURIComponent(game.id)}` : "/pricing"} key={game.id}><div><span>{localTime(game.commence_time)}</span><b>{game.matchup}</b><small>{game.away_pitcher ?? "TBD"} vs. {game.home_pitcher ?? "TBD"}</small></div><div className="gameProjection"><span>Projected score</span><b>{game.projected_score.away == null ? "—" : `${game.projected_score.away.toFixed(1)}–${game.projected_score.home?.toFixed(1)}`}</b><small>{game.home_win_probability == null ? "Unlock intelligence" : `${pct(game.home_win_probability)} home win`}</small></div></Link>)}
          </div>
        </section>
      </section>
    </Shell>
  );
}
