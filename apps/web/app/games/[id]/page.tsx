"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { API_URL, authHeaders } from "@/lib/api";
import { PickCard } from "@/components/PickCard";

export default function GameDetail() {
  const params = useParams<{id: string}>();
  const [data, setData] = useState<any>(null);
  const [message, setMessage] = useState("Loading breakdown...");

  useEffect(() => {
    fetch(`${API_URL}/api/v1/games/${params.id}`, {headers: authHeaders()})
      .then(async r => {
        const result = await r.json();
        if (!r.ok) throw new Error(result.detail ?? "Unable to load game");
        setData(result); setMessage("");
      })
      .catch(e => setMessage(e.message));
  }, [params.id]);

  if (message) return <main className="section container"><div className="card">{message}</div></main>;
  return (
    <main className="section container">
      <div className="eyebrow">Game intelligence</div>
      <h1 style={{fontSize:"58px", textAlign:"left", marginLeft:0}}>{data.game.matchup}</h1>
      <p className="section-lead">{data.game.venue} · {new Date(data.game.starts_at).toLocaleString()}</p>
      <div className="grid grid-3">
        <div className="card"><div className="muted">Away starter</div><h3>{data.game.away_probable_pitcher || "TBD"}</h3></div>
        <div className="card"><div className="muted">Home starter</div><h3>{data.game.home_probable_pitcher || "TBD"}</h3></div>
        <div className="card"><div className="muted">Market observations</div><h3>{data.odds.length}</h3></div>
      </div>
      <section className="section">
        <h2>Qualified plays</h2>
        <div className="grid">{data.picks.map((p: any) => <PickCard pick={p} key={p.id} />)}</div>
      </section>
      <section className="section">
        <h2>Latest lines</h2>
        <div className="card" style={{overflowX:"auto"}}>
          <table style={{width:"100%", borderCollapse:"collapse"}}>
            <thead><tr><th align="left">Book</th><th align="left">Market</th><th align="left">Selection</th><th align="right">Line</th><th align="right">Odds</th></tr></thead>
            <tbody>{data.odds.slice(0, 30).map((o:any, i:number) => (
              <tr key={i} style={{borderTop:"1px solid var(--line)"}}>
                <td style={{padding:"12px 0"}}>{o.bookmaker}</td><td>{o.market}</td><td>{o.selection}</td>
                <td align="right">{o.line ?? "—"}</td><td align="right">{o.price > 0 ? "+" : ""}{o.price}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
