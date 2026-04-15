"use client";

import { useState } from "react";
import { Signal, Outreach, Tone } from "@/lib/types";
import { generateOutreach } from "@/lib/outreachGenerator";
import {
  X,
  Copy,
  Check,
  MessageSquare,
  Mail,
  MessageCircle,
  Lightbulb,
  Sparkles,
  RefreshCw,
} from "lucide-react";
import { clsx } from "clsx";

interface OutreachModalProps {
  signal: Signal;
  onClose: () => void;
}

type OutreachTab = "coldDM" | "email" | "publicReply" | "contentIdea";

const tabs: { id: OutreachTab; label: string; icon: React.ElementType }[] = [
  { id: "coldDM", label: "Cold DM", icon: MessageSquare },
  { id: "email", label: "Email", icon: Mail },
  { id: "publicReply", label: "Public Reply", icon: MessageCircle },
  { id: "contentIdea", label: "Content Idea", icon: Lightbulb },
];

export default function OutreachModal({ signal, onClose }: OutreachModalProps) {
  const [activeTab, setActiveTab] = useState<OutreachTab>("coldDM");
  const [tone, setTone] = useState<Tone>("professional");
  const [outreach, setOutreach] = useState<Outreach>(() =>
    generateOutreach(signal, "professional")
  );
  const [copiedTab, setCopiedTab] = useState<string | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);

  const handleToneChange = async (newTone: Tone) => {
    setTone(newTone);
    setIsRegenerating(true);
    // Simulate generation delay
    await new Promise((r) => setTimeout(r, 500));
    setOutreach(generateOutreach(signal, newTone));
    setIsRegenerating(false);
  };

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    await new Promise((r) => setTimeout(r, 600));
    setOutreach(generateOutreach(signal, tone));
    setIsRegenerating(false);
  };

  const handleCopy = async (text: string, tab: string) => {
    await navigator.clipboard.writeText(text);
    setCopiedTab(tab);
    setTimeout(() => setCopiedTab(null), 2000);
  };

  const content = outreach[activeTab];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-3xl max-h-[85vh] bg-surface-raised border border-surface-border rounded-2xl shadow-2xl flex flex-col animate-slide-up">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-surface-border">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-brand-600/20 border border-brand-500/30 rounded-lg flex items-center justify-center">
              <Sparkles className="w-4.5 h-4.5 text-brand-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">
                Generated Outreach
              </h2>
              <p className="text-xs text-gray-500">
                For {signal.author} on{" "}
                {signal.platform.charAt(0).toUpperCase() +
                  signal.platform.slice(1)}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-500 hover:text-gray-300 hover:bg-surface-overlay rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Signal context */}
        <div className="px-5 py-3 bg-surface-overlay/30 border-b border-surface-border/50">
          <p className="text-xs text-gray-400 line-clamp-2">
            <span className="text-gray-500 font-medium">Original post: </span>
            {signal.content}
          </p>
        </div>

        {/* Tone selector */}
        <div className="flex items-center gap-3 px-5 py-3 border-b border-surface-border/50">
          <span className="text-xs text-gray-500">Tone:</span>
          {(["casual", "professional", "friendly"] as Tone[]).map((t) => (
            <button
              key={t}
              onClick={() => handleToneChange(t)}
              className={clsx(
                "px-3 py-1 rounded-full text-xs font-medium transition-all",
                tone === t
                  ? "bg-brand-600/20 text-brand-400 border border-brand-500/30"
                  : "text-gray-400 hover:text-gray-200 border border-surface-border hover:border-surface-hover"
              )}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
          <div className="flex-1" />
          <button
            onClick={handleRegenerate}
            disabled={isRegenerating}
            className="btn-ghost text-xs"
          >
            <RefreshCw
              className={`w-3.5 h-3.5 ${isRegenerating ? "animate-spin" : ""}`}
            />
            Regenerate
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-surface-border">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={clsx(
                "flex items-center gap-2 px-5 py-3 text-sm font-medium transition-all",
                activeTab === tab.id ? "tab-active" : "tab-inactive"
              )}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-5">
          {isRegenerating ? (
            <div className="space-y-3">
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className="h-4 bg-surface-overlay rounded animate-shimmer"
                  style={{ width: `${70 + Math.random() * 30}%` }}
                />
              ))}
            </div>
          ) : (
            <pre className="whitespace-pre-wrap text-sm text-gray-300 leading-relaxed font-sans">
              {content}
            </pre>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-5 border-t border-surface-border">
          <p className="text-xs text-gray-600">
            AI-generated content — review before sending
          </p>
          <div className="flex items-center gap-2">
            <button onClick={onClose} className="btn-secondary">
              Close
            </button>
            <button
              onClick={() => handleCopy(content, activeTab)}
              className="btn-primary"
            >
              {copiedTab === activeTab ? (
                <>
                  <Check className="w-4 h-4" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  Copy to Clipboard
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
