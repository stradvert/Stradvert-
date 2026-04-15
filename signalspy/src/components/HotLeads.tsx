"use client";

import { Signal } from "@/lib/types";
import { Flame, ArrowRight, Clock } from "lucide-react";

interface HotLeadsProps {
  signals: Signal[];
  onViewSignal: (signal: Signal) => void;
}

export default function HotLeads({ signals, onViewSignal }: HotLeadsProps) {
  // Top 5 highest-intent signals
  const hotSignals = [...signals]
    .filter((s) => s.intentScore >= 85)
    .sort((a, b) => b.intentScore - a.intentScore)
    .slice(0, 5);

  if (hotSignals.length === 0) return null;

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <Flame className="w-5 h-5 text-orange-400" />
        <h3 className="text-base font-semibold text-white">Hot Leads</h3>
        <span className="badge bg-orange-500/15 text-orange-400 border border-orange-500/20 ml-auto">
          {hotSignals.length} signals
        </span>
      </div>

      <div className="space-y-2">
        {hotSignals.map((signal) => (
          <button
            key={signal.id}
            onClick={() => onViewSignal(signal)}
            className="w-full flex items-center gap-3 p-3 rounded-lg bg-surface-overlay/50 hover:bg-surface-hover border border-surface-border/50 hover:border-orange-500/20 transition-all group text-left"
          >
            <div className="flex-shrink-0">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-orange-500/20 to-red-500/20 border border-orange-500/20 flex items-center justify-center">
                <span className="text-sm font-bold text-orange-400">
                  {signal.intentScore}
                </span>
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-200 truncate">
                {signal.author}
              </p>
              <p className="text-xs text-gray-500 truncate">{signal.summary}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span
                className={`text-[10px] px-1.5 py-0.5 rounded ${
                  signal.platform === "twitter"
                    ? "bg-sky-500/10 text-sky-400"
                    : signal.platform === "reddit"
                      ? "bg-orange-500/10 text-orange-400"
                      : "bg-blue-500/10 text-blue-400"
                }`}
              >
                {signal.platform}
              </span>
              <ArrowRight className="w-3.5 h-3.5 text-gray-600 group-hover:text-orange-400 transition-colors" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
