import type { Metadata } from "next";
import "./globals.css";
import "./v35.css";

export const metadata: Metadata = {
  title: { default: "EdgeBoard 3.5 — Sports Intelligence", template: "%s · EdgeBoard 3.5" },
  description: "Transparent, tracked sports-betting analytics powered by market-aware modeling.",
  icons: { icon: "/favicon.svg" }
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
