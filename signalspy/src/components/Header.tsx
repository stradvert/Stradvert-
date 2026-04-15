"use client";

import { Bell, Search, RefreshCw } from "lucide-react";
import { DashboardStats } from "@/lib/types";

interface HeaderProps {
  stats: DashboardStats;
  onRefresh: () => void;
  isRefreshing: boolean;
  notificationCount: number;
  searchValue: string;
  onSearchChange: (value: string) => void;
}

export default function Header({
  stats,
  onRefresh,
  isRefreshing,
  notificationCount,
  searchValue,
  onSearchChange,
}: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 bg-surface/80 backdrop-blur-xl border-b border-surface-border">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-6">
          {/* Stats pills */}
          <div className="flex items-center gap-3">
            <StatPill label="Signals" value={stats.totalSignals} />
            <StatPill
              label="High Intent"
              value={stats.highIntent}
              color="text-red-400"
              dot="bg-red-400"
            />
            <StatPill
              label="Saved"
              value={stats.savedLeads}
              color="text-brand-400"
              dot="bg-brand-400"
            />
            <StatPill
              label="Contacted"
              value={stats.contacted}
              color="text-emerald-400"
              dot="bg-emerald-400"
            />
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="text"
              value={searchValue}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Search signals..."
              className="input pl-9 w-64"
            />
          </div>

          {/* Refresh */}
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="btn-ghost"
            title="Scan for new signals"
          >
            <RefreshCw
              className={`w-4 h-4 ${isRefreshing ? "animate-spin" : ""}`}
            />
          </button>

          {/* Notifications */}
          <button className="btn-ghost relative">
            <Bell className="w-4 h-4" />
            {notificationCount > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-red-500 rounded-full text-[10px] font-bold text-white flex items-center justify-center">
                {notificationCount > 9 ? "9+" : notificationCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}

function StatPill({
  label,
  value,
  color = "text-gray-300",
  dot,
}: {
  label: string;
  value: number;
  color?: string;
  dot?: string;
}) {
  return (
    <div className="flex items-center gap-2 bg-surface-overlay border border-surface-border rounded-lg px-3 py-1.5">
      {dot && <span className={`glow-dot ${dot}`} />}
      <span className="text-xs text-gray-500">{label}</span>
      <span className={`text-sm font-semibold ${color}`}>{value}</span>
    </div>
  );
}
