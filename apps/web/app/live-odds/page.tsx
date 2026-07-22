"use client";

import { useEffect, useState } from "react";
import { API_URL } from "@/lib/api";

export default function LiveOddsPage() {
  const [status, setStatus] = useState<any>(null);
  useEffect(() => {
    fetch(`${API_URL}/api/v1/system/status`).then(r => r.json()).then(setStatus);
  }, []);

  return (
    <main className="section container">
      <div className="eyebrow">Data operations</div>
      <h1 style={{fontSize:"58px", textAlign:"left", marginLeft:0}}>Live odds status</h1>
      <div className="grid grid-3">
        <div className="card"><div className="stat">{status?.live_odds_configured ? "LIVE" : "SETUP"}</div><div className="muted">Odds API connection</div></div>
        <div className="card"><div className="stat">{status?.refresh_interval_minutes ?? "—"}m</div><div className="muted">Refresh interval</div></div>
        <div className="card"><div className="stat">2</div><div className="muted">FanDuel + DraftKings</div></div>
      </div>
      <section className="section">
        <h2>Recent pipeline runs</h2>
        <div className="grid">
          {(status?.recent_runs ?? []).map((run: any, index: number) => (
            <div className="card" key={index}>
              <div className="pick-top">
                <strong>{run.job}</strong>
                <span className="badge">{run.status}</span>
              </div>
              <pre className="muted" style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(run.details, null, 2)}</pre>
              {run.error && <p style={{color:"var(--danger)"}}>{run.error}</p>}
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
