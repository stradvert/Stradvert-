"use client";

import { Signal } from "@/lib/types";
import {
  Bookmark,
  BookmarkCheck,
  MessageSquare,
  Mail,
  Send,
  Sparkles,
  ExternalLink,
  CheckCircle2,
  Clock,
} from "lucide-react";
import { clsx } from "clsx";

interface SignalCardProps {
  signal: Signal;
  onGenerateOutreach: (signal: Signal) => void;
  onToggleSave: (id: string) => void;
  onMarkContacted: (id: string) => void;
}

export default function SignalCard({
  signal,
  onGenerateOutreach,
  onToggleSave,
  onMarkContacted,
}: SignalCardProps) {
  const isSaved = signal.status === "saved" || signal.status === "contacted" || signal.status === "converted";
  const isContacted = signal.status === "contacted" || signal.status === "converted";

  const timeAgo = getTimeAgo(signal.timestamp);

  const platformBadge = {
    twitter: { class: "badge-twitter", label: "Twitter/X" },
    reddit: { class: "badge-reddit", label: signal.subreddit || "Reddit" },
    linkedin: { class: "badge-linkedin", label: "LinkedIn" },
  }[signal.platform];

  const urgencyBadge = {
    high: "badge-high",
    medium: "badge-medium",
    low: "badge-low",
  }[signal.urgency];

  return (
    <div className="card-hover group animate-fade-in">
      {/* Top row — meta info */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className={platformBadge.class}>{platformBadge.label}</span>
          <span className={urgencyBadge}>
            {signal.urgency === "high" && "🔥 "}
            {signal.urgency.charAt(0).toUpperCase() + signal.urgency.slice(1)}{" "}
            Intent
          </span>
          {isContacted && (
            <span className="badge bg-emerald-500/15 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="w-3 h-3 mr-1" />
              Contacted
            </span>
          )}
        </div>
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <Clock className="w-3 h-3" />
          {timeAgo}
        </div>
      </div>

      {/* Author */}
      <div className="flex items-center gap-2 mb-3">
        <div className="w-8 h-8 rounded-full bg-surface-overlay border border-surface-border flex items-center justify-center text-xs font-semibold text-gray-400">
          {signal.author
            .replace(/^u\//, "")
            .replace(/^@/, "")
            .charAt(0)
            .toUpperCase()}
        </div>
        <div>
          <p className="text-sm font-medium text-gray-200">{signal.author}</p>
          <p className="text-xs text-gray-500">{signal.authorHandle}</p>
        </div>
      </div>

      {/* Content */}
      <p className="text-sm text-gray-300 leading-relaxed mb-3">
        {signal.content}
      </p>

      {/* Summary */}
      <div className="bg-surface-overlay/50 border border-surface-border/50 rounded-lg px-3 py-2 mb-3">
        <p className="text-xs text-gray-400">
          <Sparkles className="w-3 h-3 inline mr-1 text-brand-400" />
          {signal.summary}
        </p>
      </div>

      {/* Intent Score Bar */}
      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-gray-500">Intent Score</span>
          <span
            className={clsx("text-sm font-bold", {
              "text-red-400": signal.intentScore >= 80,
              "text-amber-400":
                signal.intentScore >= 50 && signal.intentScore < 80,
              "text-emerald-400": signal.intentScore < 50,
            })}
          >
            {signal.intentScore}/100
          </span>
        </div>
        <div className="intent-bar">
          <div
            className={clsx("intent-fill", {
              "bg-gradient-to-r from-red-500 to-red-400":
                signal.intentScore >= 80,
              "bg-gradient-to-r from-amber-500 to-amber-400":
                signal.intentScore >= 50 && signal.intentScore < 80,
              "bg-gradient-to-r from-emerald-500 to-emerald-400":
                signal.intentScore < 50,
            })}
            style={{ width: `${signal.intentScore}%` }}
          />
        </div>
      </div>

      {/* Keywords */}
      <div className="flex items-center gap-1.5 mb-4 flex-wrap">
        {signal.keywords.map((kw) => (
          <span
            key={kw}
            className="px-2 py-0.5 bg-surface-overlay text-gray-400 rounded text-[11px] border border-surface-border"
          >
            {kw}
          </span>
        ))}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2 pt-3 border-t border-surface-border/50">
        <button
          onClick={() => onGenerateOutreach(signal)}
          className="btn-primary text-xs py-1.5 flex-1"
        >
          <Sparkles className="w-3.5 h-3.5" />
          Generate Outreach
        </button>
        <button
          onClick={() => onToggleSave(signal.id)}
          className={clsx(
            "btn-ghost p-2",
            isSaved ? "text-brand-400" : "text-gray-500"
          )}
          title={isSaved ? "Saved" : "Save lead"}
        >
          {isSaved ? (
            <BookmarkCheck className="w-4 h-4" />
          ) : (
            <Bookmark className="w-4 h-4" />
          )}
        </button>
        {!isContacted && (
          <button
            onClick={() => onMarkContacted(signal.id)}
            className="btn-ghost p-2 text-gray-500"
            title="Mark as contacted"
          >
            <Send className="w-4 h-4" />
          </button>
        )}
        <a
          href={signal.url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-ghost p-2 text-gray-500"
          title="View original post"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}

function getTimeAgo(timestamp: string): string {
  const now = Date.now();
  const then = new Date(timestamp).getTime();
  const diff = now - then;

  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "Just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  return `${days}d ago`;
}
