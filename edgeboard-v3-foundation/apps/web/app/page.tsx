import Link from "next/link";
import { PickCard } from "@/components/PickCard";
import { getFreePick } from "@/lib/api";

export default async function Home() {
  const freePick = await getFreePick();
  return (
    <main>
      <section className="hero container">
        <div className="eyebrow">Professional MLB intelligence</div>
        <h1>Find the edge before the market does.</h1>
        <p>
          EdgeBoard transforms odds, projections, and model signals into a clear,
          disciplined betting workflow built for serious subscribers.
        </p>
        <div className="actions">
          <Link className="button primary" href="/register">Start free</Link>
          <Link className="button" href="/pricing">View plans</Link>
        </div>
      </section>

      <section className="section container">
        <div className="grid grid-3">
          <div className="card"><div className="stat">24/7</div><div className="muted">Automated market monitoring</div></div>
          <div className="card"><div className="stat">100%</div><div className="muted">Transparent tracked performance</div></div>
          <div className="card"><div className="stat">MLB</div><div className="muted">Built first, multi-sport architecture next</div></div>
        </div>
      </section>

      <section className="section container">
        <h2>Today&apos;s free preview</h2>
        <p className="section-lead">One model-qualified preview. Subscribers unlock the full card and game intelligence.</p>
        {freePick ? <PickCard pick={freePick} /> : <div className="card">The API is waking up. Refresh shortly.</div>}
      </section>

      <section className="section container">
        <h2>Built for decisions, not hype.</h2>
        <div className="grid grid-3">
          <div className="card"><h3>Model edge</h3><p className="muted">Compare projected probability against the sportsbook market.</p></div>
          <div className="card"><h3>Risk sizing</h3><p className="muted">Convert model conviction into conservative unit recommendations.</p></div>
          <div className="card"><h3>Accountability</h3><p className="muted">Track every published pick, result, ROI, and closing-line signal.</p></div>
        </div>
      </section>
    </main>
  );
}
