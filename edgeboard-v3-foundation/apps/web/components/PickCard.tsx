import type { Pick } from "@/lib/api";

export function PickCard({ pick }: { pick: Pick }) {
  return (
    <article className="card">
      <div className="pick-top">
        <div>
          <div className="eyebrow">{pick.sportsbook}</div>
          <h3>{pick.matchup}</h3>
          <div className="muted">{pick.selection} · {pick.american_odds > 0 ? "+" : ""}{pick.american_odds}</div>
        </div>
        <span className="badge">{pick.confidence.toFixed(0)} confidence</span>
      </div>
      <div className="metrics">
        <div className="metric"><span className="muted">Edge</span><strong>{pick.edge_percent.toFixed(1)}%</strong></div>
        <div className="metric"><span className="muted">EV</span><strong>{pick.expected_value_percent.toFixed(1)}%</strong></div>
        <div className="metric"><span className="muted">Model</span><strong>{(pick.model_probability * 100).toFixed(1)}%</strong></div>
        <div className="metric"><span className="muted">Stake</span><strong>{pick.units.toFixed(2)}u</strong></div>
      </div>
      <p className="muted">{pick.explanation}</p>
    </article>
  );
}
