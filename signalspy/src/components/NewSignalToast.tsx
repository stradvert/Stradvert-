"use client";

import { Signal } from "@/lib/types";
import { Zap, X } from "lucide-react";

interface NewSignalToastProps {
  signal: Signal;
  onDismiss: () => void;
  onView: () => void;
}

export default function NewSignalToast({
  signal,
  onDismiss,
  onView,
}: NewSignalToastProps) {
  return (
    <div className="fixed top-4 right-4 z-50 w-96 animate-slide-up">
      <div className="bg-surface-raised border border-brand-500/30 rounded-xl p-4 shadow-xl shadow-brand-500/10">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 bg-brand-600/20 rounded-lg flex items-center justify-center flex-shrink-0">
            <Zap className="w-4 h-4 text-brand-400" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white">New Signal Detected</p>
            <p className="text-xs text-gray-400 mt-0.5 truncate">
              {signal.author} on {signal.platform}
            </p>
            <p className="text-xs text-gray-500 mt-1 line-clamp-2">
              {signal.summary}
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs font-medium text-brand-400">
                Score: {signal.intentScore}/100
              </span>
              <button
                onClick={onView}
                className="text-xs text-brand-400 hover:text-brand-300 font-medium"
              >
                View signal →
              </button>
            </div>
          </div>
          <button
            onClick={onDismiss}
            className="p-1 text-gray-600 hover:text-gray-400 transition-colors flex-shrink-0"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
