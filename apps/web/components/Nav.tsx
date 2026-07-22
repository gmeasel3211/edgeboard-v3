import Link from "next/link";

export function Nav() {
  return (
    <nav className="nav">
      <div className="container nav-inner">
        <Link href="/" className="brand">Edge<span>Board</span></Link>
        <div className="nav-links">
          <Link href="/dashboard">Card</Link>
          <Link href="/games">Games</Link>
          <Link href="/live-odds">Live Odds</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/login" className="button">Log in</Link>
        </div>
      </div>
    </nav>
  );
}
