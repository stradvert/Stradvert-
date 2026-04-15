"use client";

import { FilterState, Platform } from "@/lib/types";
import { Filter, X } from "lucide-react";

interface FilterBarProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  allKeywords: string[];
}

export default function FilterBar({
  filters,
  onFilterChange,
  allKeywords,
}: FilterBarProps) {
  const hasActiveFilters =
    filters.platform !== "all" ||
    filters.keyword !== "" ||
    filters.intentLevel !== "all" ||
    filters.status !== "all";

  const update = (patch: Partial<FilterState>) => {
    onFilterChange({ ...filters, ...patch });
  };

  return (
    <div className="flex items-center gap-3 flex-wrap">
      <div className="flex items-center gap-1.5 text-gray-500 text-sm">
        <Filter className="w-4 h-4" />
        <span>Filters</span>
      </div>

      {/* Platform filter */}
      <select
        value={filters.platform}
        onChange={(e) =>
          update({ platform: e.target.value as Platform | "all" })
        }
        className="select w-auto"
      >
        <option value="all">All Platforms</option>
        <option value="twitter">Twitter/X</option>
        <option value="reddit">Reddit</option>
        <option value="linkedin">LinkedIn</option>
      </select>

      {/* Intent level */}
      <select
        value={filters.intentLevel}
        onChange={(e) =>
          update({
            intentLevel: e.target.value as "all" | "high" | "medium" | "low",
          })
        }
        className="select w-auto"
      >
        <option value="all">All Intent Levels</option>
        <option value="high">High Intent (80+)</option>
        <option value="medium">Medium Intent (50-79)</option>
        <option value="low">Low Intent (&lt;50)</option>
      </select>

      {/* Keyword filter */}
      <select
        value={filters.keyword}
        onChange={(e) => update({ keyword: e.target.value })}
        className="select w-auto"
      >
        <option value="">All Keywords</option>
        {allKeywords.map((kw) => (
          <option key={kw} value={kw}>
            {kw}
          </option>
        ))}
      </select>

      {/* Status filter */}
      <select
        value={filters.status}
        onChange={(e) =>
          update({
            status: e.target.value as FilterState["status"],
          })
        }
        className="select w-auto"
      >
        <option value="all">All Status</option>
        <option value="new">New</option>
        <option value="saved">Saved</option>
        <option value="contacted">Contacted</option>
        <option value="converted">Converted</option>
      </select>

      {/* Clear filters */}
      {hasActiveFilters && (
        <button
          onClick={() =>
            onFilterChange({
              platform: "all",
              keyword: "",
              intentLevel: "all",
              status: "all",
              search: filters.search,
            })
          }
          className="btn-ghost text-xs text-red-400 hover:text-red-300"
        >
          <X className="w-3.5 h-3.5" />
          Clear
        </button>
      )}
    </div>
  );
}
