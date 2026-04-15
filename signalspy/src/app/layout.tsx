import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SignalSpy — Buying Signal Intelligence",
  description:
    "Monitor online platforms and surface high-intent buying signals for actionable outreach.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
