import Link from "next/link";
import { currentUser } from "@/lib/auth";
import { Logo } from "./logo";
import { LogoutButton } from "./logout-button";

export async function Shell({ children }: { children: React.ReactNode }) {
  const user = await currentUser(true);
  return (
    <>
      <nav className="siteNav v35Nav">
        <div className="brandWrap"><Logo /><span className="versionBadge">3.5</span></div>
        <div className="navLinks">
          {user ? <Link href="/dashboard">Today</Link> : <Link href="/">Home</Link>}
          {user && user.tier !== "free" && <Link href="/performance">Performance</Link>}
          <Link href="/pricing">Membership</Link>
          {user && <Link href="/account">Account</Link>}
          {user?.role === "admin" && <Link href="/live-odds">System Health</Link>}
          {user?.role === "admin" && <Link href="/admin">Admin</Link>}
        </div>
        <div className="navActions">
          {user ? (
            <>
              <span className="tierPill">{user.role === "admin" ? "ADMIN" : user.tier.toUpperCase()}</span>
              <LogoutButton />
            </>
          ) : (
            <>
              <Link className="navButton" href="/login">Log in</Link>
              <Link className="button buttonSmall" href="/register">Start free</Link>
            </>
          )}
        </div>
      </nav>
      <main>{children}</main>
      <footer className="footer v35Footer">
        <div className="brandWrap"><Logo /><span className="versionBadge">3.5</span></div>
        <p>Market-aware analytics. Transparent records. No guarantees.</p>
        <div><Link href="/pricing">Membership</Link><span>© 2026 EdgeBoard</span></div>
      </footer>
    </>
  );
}
