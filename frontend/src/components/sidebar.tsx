"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/devices", label: "Devices" },
  { href: "/telemetry", label: "Telemetry" },
  { href: "/network", label: "Network" },
  { href: "/attacks", label: "Attacks" },
  { href: "/ai-center", label: "AI Center" },
  { href: "/trust-center", label: "Trust Center" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 shrink-0 border-r bg-sidebar text-sidebar-foreground">
      <div className="border-b px-5 py-4">
        <p className="text-sm font-semibold tracking-wide">SentinelIoT</p>
      </div>
      <nav className="flex flex-col gap-1 p-3">
        {links.map((link) => {
          const isActive = pathname === link.href;

          return (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-md px-3 py-2 text-sm transition-colors ${
                isActive
                  ? "bg-sidebar-primary text-sidebar-primary-foreground"
                  : "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              }`}
            >
              {link.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
