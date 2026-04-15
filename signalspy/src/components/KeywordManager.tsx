"use client";

import { useState } from "react";
import { Keyword } from "@/lib/types";
import { Plus, X, Tag, ToggleLeft, ToggleRight } from "lucide-react";

interface KeywordManagerProps {
  keywords: Keyword[];
  onAddKeyword: (text: string) => void;
  onRemoveKeyword: (id: string) => void;
  onToggleKeyword: (id: string) => void;
}

export default function KeywordManager({
  keywords,
  onAddKeyword,
  onRemoveKeyword,
  onToggleKeyword,
}: KeywordManagerProps) {
  const [newKeyword, setNewKeyword] = useState("");

  const handleAdd = () => {
    const trimmed = newKeyword.trim();
    if (trimmed && !keywords.some((k) => k.text.toLowerCase() === trimmed.toLowerCase())) {
      onAddKeyword(trimmed);
      setNewKeyword("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleAdd();
    }
  };

  const activeCount = keywords.filter((k) => k.isActive).length;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Tag className="w-5 h-5 text-brand-400" />
            Tracked Keywords
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            {activeCount} active keyword{activeCount !== 1 ? "s" : ""} being
            monitored
          </p>
        </div>
      </div>

      {/* Add keyword input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={newKeyword}
          onChange={(e) => setNewKeyword(e.target.value)}
          onKeyDown={handleKeyDown}
          className="input flex-1"
          placeholder='Add a keyword (e.g. "AI tools", "dentist marketing")'
        />
        <button
          onClick={handleAdd}
          disabled={!newKeyword.trim()}
          className="btn-primary"
        >
          <Plus className="w-4 h-4" />
          Add
        </button>
      </div>

      {/* Keywords grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {keywords.map((keyword) => (
          <div
            key={keyword.id}
            className={`flex items-center justify-between gap-2 px-3 py-2.5 rounded-lg border transition-all ${
              keyword.isActive
                ? "bg-brand-600/10 border-brand-500/20 text-brand-300"
                : "bg-surface-overlay border-surface-border text-gray-500"
            }`}
          >
            <span className="text-sm font-medium truncate">{keyword.text}</span>
            <div className="flex items-center gap-1 flex-shrink-0">
              <button
                onClick={() => onToggleKeyword(keyword.id)}
                className="p-1 hover:bg-surface-overlay/50 rounded transition-colors"
                title={keyword.isActive ? "Deactivate" : "Activate"}
              >
                {keyword.isActive ? (
                  <ToggleRight className="w-5 h-5 text-brand-400" />
                ) : (
                  <ToggleLeft className="w-5 h-5 text-gray-600" />
                )}
              </button>
              <button
                onClick={() => onRemoveKeyword(keyword.id)}
                className="p-1 hover:bg-red-500/10 rounded text-gray-600 hover:text-red-400 transition-colors"
                title="Remove keyword"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {keywords.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <Tag className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">No keywords yet. Add some to start monitoring!</p>
        </div>
      )}
    </div>
  );
}
