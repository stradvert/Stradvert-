"use client";

import { Signal } from "@/lib/types";
import { TrendingUp, Users, Zap, Target, ArrowUpRight } from "lucide-react";

interface StatsOverviewProps {
  signals: Signal[];
}

export default function StatsOverview({ signals }: StatsOverviewProps) {
  const totalSignals = signals.length;
  const highIntent = signals.filter((s) => s.intentScore >= 80).length;
  const savedLeads = signals.filter(
    (s) => s.status === "saved" || s.status === "contacted" || s.status === "converted"
  ).length;
  const contacted = signals.filter(
    (s) => s.status === "contacted" || s.status === "converted"
  ).length;

  const avgScore = signals.length
    ? Math.round(signals.reduce((sum, s) => sum + s.intentScore, 0) / signals.length)
    : 0;

  const platformBreakdown = {
    twitter: signals.filter((s) => s.platform === "twitter").length,
    reddit: signals.filter((s) => s.platform === "reddit").length,
    linkedin: signals.filter((s) => s.platform === "linkedin").length,
  };

  const stats = [
    {
      label: "Total Signals",
      value: totalSignals,
      icon: Zap,
      color: "text-brand-400",
      bgColor: "bg-brand-500/10",
      borderColor: "border-brand-500/20",
      change: "+12%",
    },
    {
      label: "High Intent",
      value: highIntent,
      icon: Target,
      color: "text-red-400",
      bgColor: "bg-red-500/10",
      borderColor: "border-red-500/20",
      change: "+8%",
    },
    {
      label: "Saved Leads",
      value: savedLeads,
      icon: Users,
      color: "text-amber-400",
      bgColor: "bg-amber-500/10",
      borderColor: "border-amber-500/20",
      change: "+5",
    },
    {
      label: "Avg. Score",
      value: avgScore,
      icon: TrendingUp,
      color: "text-emerald-400",
      bgColor: "bg-emerald-500/10",
      borderColor: "border-emerald-500/20",
      change: "+3pts",
    },
  ];

  return (
    <div className="space-y-4">
      {/* Main stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {stats.map((stat) => (
          <div key={stat.label} className="card">
            <div className="flex items-center justify-between mb-3">
              <div
                className={`w-9 h-9 ${stat.bgColor} ${stat.borderColor} border rounded-lg flex items-center justify-center`}
              >
                <stat.icon className={`w-4.5 h-4.5 ${stat.color}`} />
              </div>
              <span className="flex items-center gap-0.5 text-xs text-emerald-400">
                <ArrowUpRight className="w-3 h-3" />
                {stat.change}
              </span>
            </div>
            <p className="text-2xl font-bold text-white">{stat.value}</p>
            <p className="text-xs text-gray-500 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Platform breakdown */}
      <div className="card">
        <h3 className="text-sm font-medium text-gray-400 mb-3">
          Platform Distribution
        </h3>
        <div className="flex gap-4">
          {(
            [
              { platform: "Twitter/X", count: platformBreakdown.twitter, color: "bg-sky-500" },
              { platform: "Reddit", count: platformBreakdown.reddit, color: "bg-orange-500" },
              { platform: "LinkedIn", count: platformBreakdown.linkedin, color: "bg-blue-500" },
            ] as const
          ).map((item) => (
            <div key={item.platform} className="flex-1">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs text-gray-400">{item.platform}</span>
                <span className="text-xs font-medium text-gray-300">
                  {item.count}
                </span>
              </div>
              <div className="h-1.5 bg-surface-overlay rounded-full overflow-hidden">
                <div
                  className={`h-full ${item.color} rounded-full transition-all duration-500`}
                  style={{
                    width: `${totalSignals ? (item.count / totalSignals) * 100 : 0}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
