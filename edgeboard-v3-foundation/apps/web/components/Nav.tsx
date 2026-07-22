import Link from "next/link";

export function Nav() {
  return (
    <nav className="nav">
      <div className="container nav-inner">
        <Link href="/" className="brand">Edge<span>Board</span></Link>
        <div className="nav-links">
          <Link href="/pricing">Pricing</Link>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/login" className="button">Log in</Link>
          <Link href="/register" className="button primary">Start free</Link>
        </div>
      </div>
    </nav>
  );
}
