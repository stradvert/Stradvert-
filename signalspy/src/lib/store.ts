import { Signal, Keyword, FilterState, User } from "./types";
import { allSignals, defaultKeywords, generateNewSignal } from "./mockData";

// In-memory store for the prototype (persisted to localStorage on client)
const STORAGE_KEYS = {
  signals: "signalspy_signals",
  keywords: "signalspy_keywords",
  user: "signalspy_user",
} as const;

export function getStoredSignals(): Signal[] {
  if (typeof window === "undefined") return allSignals;
  const stored = localStorage.getItem(STORAGE_KEYS.signals);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      return allSignals;
    }
  }
  localStorage.setItem(STORAGE_KEYS.signals, JSON.stringify(allSignals));
  return allSignals;
}

export function saveSignals(signals: Signal[]): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEYS.signals, JSON.stringify(signals));
}

export function getStoredKeywords(): Keyword[] {
  if (typeof window === "undefined") return defaultKeywords;
  const stored = localStorage.getItem(STORAGE_KEYS.keywords);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      return defaultKeywords;
    }
  }
  localStorage.setItem(STORAGE_KEYS.keywords, JSON.stringify(defaultKeywords));
  return defaultKeywords;
}

export function saveKeywords(keywords: Keyword[]): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEYS.keywords, JSON.stringify(keywords));
}

export function getStoredUser(): User | null {
  if (typeof window === "undefined") return null;
  const stored = localStorage.getItem(STORAGE_KEYS.user);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      return null;
    }
  }
  return null;
}

export function saveUser(user: User | null): void {
  if (typeof window === "undefined") return;
  if (user) {
    localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user));
  } else {
    localStorage.removeItem(STORAGE_KEYS.user);
  }
}

export function clearAllData(): void {
  if (typeof window === "undefined") return;
  Object.values(STORAGE_KEYS).forEach((key) => localStorage.removeItem(key));
}

export function filterSignals(
  signals: Signal[],
  filters: FilterState
): Signal[] {
  return signals.filter((signal) => {
    if (filters.platform !== "all" && signal.platform !== filters.platform)
      return false;

    if (filters.keyword) {
      const kw = filters.keyword.toLowerCase();
      const matchesKeyword = signal.keywords.some((k) =>
        k.toLowerCase().includes(kw)
      );
      const matchesContent = signal.content.toLowerCase().includes(kw);
      if (!matchesKeyword && !matchesContent) return false;
    }

    if (filters.intentLevel !== "all") {
      if (filters.intentLevel === "high" && signal.intentScore < 80)
        return false;
      if (
        filters.intentLevel === "medium" &&
        (signal.intentScore < 50 || signal.intentScore >= 80)
      )
        return false;
      if (filters.intentLevel === "low" && signal.intentScore >= 50)
        return false;
    }

    if (filters.status !== "all" && signal.status !== filters.status)
      return false;

    if (filters.search) {
      const s = filters.search.toLowerCase();
      return (
        signal.content.toLowerCase().includes(s) ||
        signal.author.toLowerCase().includes(s) ||
        signal.summary.toLowerCase().includes(s)
      );
    }

    return true;
  });
}

export function exportToCSV(signals: Signal[]): string {
  const headers = [
    "ID",
    "Platform",
    "Author",
    "Handle",
    "Content",
    "URL",
    "Timestamp",
    "Intent Score",
    "Urgency",
    "Keywords",
    "Summary",
    "Status",
  ];

  const rows = signals.map((s) => [
    s.id,
    s.platform,
    s.author,
    s.authorHandle,
    `"${s.content.replace(/"/g, '""')}"`,
    s.url,
    s.timestamp,
    s.intentScore.toString(),
    s.urgency,
    s.keywords.join("; "),
    `"${s.summary.replace(/"/g, '""')}"`,
    s.status,
  ]);

  return [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
}

export { generateNewSignal };
