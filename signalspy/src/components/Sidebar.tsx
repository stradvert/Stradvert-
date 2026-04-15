"use client";

import {
  Radio,
  LayoutDashboard,
  Users,
  Settings,
  LogOut,
  Search,
  Zap,
  Tag,
} from "lucide-react";
import { clsx } from "clsx";

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  onLogout: () => void;
  userName: string;
  userEmail: string;
}

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "signals", label: "Signal Feed", icon: Zap },
  { id: "leads", label: "Saved Leads", icon: Users },
  { id: "keywords", label: "Keywords", icon: Tag },
];

export default function Sidebar({
  activeTab,
  onTabChange,
  onLogout,
  userName,
  userEmail,
}: SidebarProps) {
  return (
    <aside className="w-64 bg-surface-raised border-r border-surface-border flex flex-col h-screen sticky top-0">
      {/* Logo */}
      <div className="p-5 border-b border-surface-border">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-brand-600 rounded-xl flex items-center justify-center">
            <Radio className="w-4.5 h-4.5 text-white" />
          </div>
          <div>
            <span className="text-lg font-bold text-white">SignalSpy</span>
            <span className="block text-[10px] text-gray-500 -mt-0.5 tracking-wider uppercase">
              Intelligence
            </span>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onTabChange(item.id)}
            className={clsx(
              "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150",
              activeTab === item.id
                ? "bg-brand-600/15 text-brand-400 border border-brand-500/20"
                : "text-gray-400 hover:text-gray-200 hover:bg-surface-overlay"
            )}
          >
            <item.icon className="w-4.5 h-4.5" />
            {item.label}
          </button>
        ))}
      </nav>

      {/* User section */}
      <div className="p-3 border-t border-surface-border">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 rounded-full bg-brand-600/20 border border-brand-500/30 flex items-center justify-center">
            <span className="text-xs font-semibold text-brand-400">
              {userName
                .split(" ")
                .map((n) => n[0])
                .join("")
                .toUpperCase()
                .slice(0, 2)}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-200 truncate">
              {userName}
            </p>
            <p className="text-xs text-gray-500 truncate">{userEmail}</p>
          </div>
          <button
            onClick={onLogout}
            className="p-1.5 text-gray-500 hover:text-red-400 rounded-lg hover:bg-red-500/10 transition-all"
            title="Sign out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
