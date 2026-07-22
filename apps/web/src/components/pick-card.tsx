import Link from "next/link";
import type { Pick } from "@/lib/types";
import { localTime, marketName, odds, pct } from "@/lib/format";

export function PickCard({ pick, locked = false }: { pick: Pick; locked?: boolean }) {
  const breakEven = pick.price > 0 ? 100 / (pick.price + 100) : Math.abs(pick.price) / (Math.abs(pick.price) + 100);
  const confidence = Math.max(0, Math.min(100, pick.confidence * 100));
  const reasons = pick.reasons.filter((reason) => !reason.toLowerCase().startsWith("risk:"));
  const risks = pick.reasons.filter((reason) => reason.toLowerCase().startsWith("risk:"));

  return (
    <article className="pickCard v35PickCard">
      <div className="pickTop">
        <span className={`grade grade${pick.grade.replace("+", "Plus")}`}>{pick.grade}</span>
        <div className="pickIdentity">
          <span className="eyebrow">{marketName(pick.market)} · BEST AT {pick.bookmaker.toUpperCase()}</span>
          <h3>{pick.selection}{pick.line == null ? "" : ` ${pick.line > 0 ? "+" : ""}${pick.line}`}</h3>
          <p>{pick.matchup} · {localTime(pick.commence_time)}</p>
        </div>
        <div className="pickPriceBlock"><span>Current price</span><strong className="price">{odds(pick.price)}</strong></div>
      </div>

      <div className="decisionStrip">
        <div><span>Model probability</span><b>{pct(pick.model_probability)}</b></div>
        <div><span>Break-even</span><b>{(breakEven * 100).toFixed(1)}%</b></div>
        <div><span>Edge</span><b className="positive">+{pct(pick.edge)}</b></div>
        <div><span>Expected value</span><b className="positive">+{pct(pick.expected_value)}</b></div>
      </div>

      <div className="pickGrid v35PickGrid">
        <div><span>Fair line</span><b>{odds(pick.fair_odds)}</b></div>
        <div><span>Recommended stake</span><b>{pick.units.toFixed(2)}u</b></div>
        <div><span>Confidence</span><b>{confidence.toFixed(0)}%</b></div>
        <div><span>Data quality</span><b>{pick.data_quality}/100</b></div>
      </div>

      <div className="confidenceHeader"><span>Confidence profile</span><b>{confidence.toFixed(0)}%</b></div>
      <div className="confidenceTrack"><i style={{ width: `${confidence}%` }} /></div>

      {locked ? (
        <div className="lockedNote">Upgrade to unlock the full model explanation, risk factors, game intelligence, and every official play.</div>
      ) : (
        <>
          <div className="analysisGrid">
            <section><span className="eyebrow">WHY THE MODEL LIKES IT</span><ul className="reasonList">{reasons.slice(0, 6).map((reason) => <li key={reason}>{reason}</li>)}</ul></section>
            <section><span className="eyebrow riskEyebrow">WHAT CAN GO WRONG</span>{risks.length ? <ul className="reasonList riskList">{risks.map((reason) => <li key={reason}>{reason.replace(/^Risk:\s*/i, "")}</li>)}</ul> : <p className="mutedCopy">No specific risk flag was generated beyond normal market variance.</p>}</section>
          </div>
          <div className="pickMeta"><span>Best book: {pick.bookmaker}</span><span>Break-even: {(breakEven * 100).toFixed(1)}%</span><span>Data quality: {pick.data_quality}/100</span></div>
          <Link className="textLink intelligenceLink" href={`/game/${encodeURIComponent(pick.game_id)}`}>Open full game intelligence →</Link>
        </>
      )}
    </article>
  );
}
