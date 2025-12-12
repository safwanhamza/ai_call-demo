import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Voice Agent",
  description: "AI Voice Agent Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased flex h-screen">
        <aside className="w-64 bg-gray-900 text-white flex flex-col">
            <div className="p-4 font-bold text-xl border-b border-gray-700">AI Voice Agent</div>
            <nav className="flex-1 p-4 space-y-2">
                <Link href="/" className="block py-2 px-4 rounded hover:bg-gray-800">Dashboard</Link>
                <Link href="/scripts" className="block py-2 px-4 rounded hover:bg-gray-800">Scripts</Link>
                <Link href="/voice-cloning" className="block py-2 px-4 rounded hover:bg-gray-800 text-gray-500 cursor-not-allowed">Voice Cloning (Soon)</Link>
            </nav>
            <div className="p-4 border-t border-gray-700 text-sm text-gray-400">
                Logged in as Admin
            </div>
        </aside>
        <div className="flex-1 overflow-auto">
            {children}
        </div>
      </body>
    </html>
  );
}
