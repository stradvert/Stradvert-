"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import {
  Signal,
  Keyword,
  FilterState,
  DashboardStats,
  User,
} from "@/lib/types";
import {
  getStoredSignals,
  saveSignals,
  getStoredKeywords,
  saveKeywords,
  getStoredUser,
  saveUser,
  filterSignals,
  exportToCSV,
  generateNewSignal,
} from "@/lib/store";

import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import FilterBar from "@/components/FilterBar";
import SignalCard from "@/components/SignalCard";
import OutreachModal from "@/components/OutreachModal";
import KeywordManager from "@/components/KeywordManager";
import HotLeads from "@/components/HotLeads";
import StatsOverview from "@/components/StatsOverview";
import NewSignalToast from "@/components/NewSignalToast";
import {
  Download,
  Zap,
  Inbox,
  Radio,
  Users,
  ChevronDown,
} from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [keywords, setKeywords] = useState<Keyword[]>([]);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [filters, setFilters] = useState<FilterState>({
    platform: "all",
    keyword: "",
    intentLevel: "all",
    status: "all",
    search: "",
  });
  const [outreachSignal, setOutreachSignal] = useState<Signal | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [newSignalToast, setNewSignalToast] = useState<Signal | null>(null);
  const [visibleCount, setVisibleCount] = useState(10);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Auth check
  useEffect(() => {
    const storedUser = getStoredUser();
    if (!storedUser) {
      router.replace("/login");
      return;
    }
    setUser(storedUser);
    setSignals(getStoredSignals());
    setKeywords(getStoredKeywords());
  }, [router]);

  // Real-time signal simulation — new signal every 30s
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      const newSignal = generateNewSignal();
      setSignals((prev) => {
        const updated = [newSignal, ...prev];
        saveSignals(updated);
        return updated;
      });
      setNewSignalToast(newSignal);
      // Auto-dismiss after 5s
      setTimeout(() => setNewSignalToast(null), 5000);
    }, 30000);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const handleRefresh = useCallback(async () => {
    setIsRefreshing(true);
    // Simulate scanning delay
    await new Promise((r) => setTimeout(r, 1500));
    const newSignal = generateNewSignal();
    setSignals((prev) => {
      const updated = [newSignal, ...prev];
      saveSignals(updated);
      return updated;
    });
    setNewSignalToast(newSignal);
    setTimeout(() => setNewSignalToast(null), 5000);
    setIsRefreshing(false);
  }, []);

  const handleToggleSave = useCallback((id: string) => {
    setSignals((prev) => {
      const updated = prev.map((s) =>
        s.id === id
          ? { ...s, status: s.status === "new" ? ("saved" as const) : ("new" as const) }
          : s
      );
      saveSignals(updated);
      return updated;
    });
  }, []);

  const handleMarkContacted = useCallback((id: string) => {
    setSignals((prev) => {
      const updated = prev.map((s) =>
        s.id === id ? { ...s, status: "contacted" as const } : s
      );
      saveSignals(updated);
      return updated;
    });
  }, []);

  const handleAddKeyword = useCallback(
    (text: string) => {
      const newKeyword: Keyword = {
        id: `kw-${Date.now()}`,
        text,
        isActive: true,
        createdAt: new Date().toISOString(),
      };
      const updated = [...keywords, newKeyword];
      setKeywords(updated);
      saveKeywords(updated);
    },
    [keywords]
  );

  const handleRemoveKeyword = useCallback(
    (id: string) => {
      const updated = keywords.filter((k) => k.id !== id);
      setKeywords(updated);
      saveKeywords(updated);
    },
    [keywords]
  );

  const handleToggleKeyword = useCallback(
    (id: string) => {
      const updated = keywords.map((k) =>
        k.id === id ? { ...k, isActive: !k.isActive } : k
      );
      setKeywords(updated);
      saveKeywords(updated);
    },
    [keywords]
  );

  const handleExportCSV = useCallback(() => {
    const toExport =
      activeTab === "leads"
        ? signals.filter(
            (s) =>
              s.status === "saved" ||
              s.status === "contacted" ||
              s.status === "converted"
          )
        : filteredSignals;

    const csv = exportToCSV(toExport);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute(
      "download",
      `signalspy-export-${new Date().toISOString().slice(0, 10)}.csv`
    );
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }, [signals, activeTab]);

  const handleLogout = useCallback(() => {
    saveUser(null);
    router.replace("/login");
  }, [router]);

  // Compute filtered signals
  const filteredSignals = filterSignals(signals, filters);

  // For leads tab, show only saved/contacted
  const leadsSignals = signals.filter(
    (s) =>
      s.status === "saved" ||
      s.status === "contacted" ||
      s.status === "converted"
  );

  const stats: DashboardStats = {
    totalSignals: signals.length,
    highIntent: signals.filter((s) => s.intentScore >= 80).length,
    savedLeads: leadsSignals.length,
    contacted: signals.filter(
      (s) => s.status === "contacted" || s.status === "converted"
    ).length,
  };

  const allKeywordTexts = Array.from(
    new Set(signals.flatMap((s) => s.keywords))
  ).sort();

  if (!user) return null;

  const displaySignals =
    activeTab === "leads" ? leadsSignals : filteredSignals;
  const visibleSignals = displaySignals.slice(0, visibleCount);

  return (
    <div className="flex min-h-screen">
      <Sidebar
        activeTab={activeTab}
        onTabChange={(tab) => {
          setActiveTab(tab);
          setVisibleCount(10);
        }}
        onLogout={handleLogout}
        userName={user.name}
        userEmail={user.email}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <Header
          stats={stats}
          onRefresh={handleRefresh}
          isRefreshing={isRefreshing}
          notificationCount={signals.filter((s) => s.intentScore >= 90 && s.status === "new").length}
          searchValue={filters.search}
          onSearchChange={(search) => setFilters((f) => ({ ...f, search }))}
        />

        <main className="flex-1 p-6 overflow-y-auto">
          {/* Dashboard overview */}
          {activeTab === "dashboard" && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-xl font-bold text-white">
                    Welcome back, {user.name.split(" ")[0]}
                  </h1>
                  <p className="text-sm text-gray-500 mt-0.5">
                    Here&apos;s what&apos;s happening with your signals today.
                  </p>
                </div>
                <button onClick={handleExportCSV} className="btn-secondary">
                  <Download className="w-4 h-4" />
                  Export CSV
                </button>
              </div>

              <StatsOverview signals={signals} />

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Hot Leads panel */}
                <div className="lg:col-span-1">
                  <HotLeads
                    signals={signals.filter((s) => s.status === "new")}
                    onViewSignal={(signal) => setOutreachSignal(signal)}
                  />
                </div>

                {/* Recent high-intent signals */}
                <div className="lg:col-span-2">
                  <div className="card">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-base font-semibold text-white flex items-center gap-2">
                        <Zap className="w-5 h-5 text-brand-400" />
                        Recent High-Intent Signals
                      </h3>
                      <button
                        onClick={() => {
                          setActiveTab("signals");
                          setFilters((f) => ({
                            ...f,
                            intentLevel: "high",
                          }));
                        }}
                        className="text-xs text-brand-400 hover:text-brand-300"
                      >
                        View all →
                      </button>
                    </div>
                    <div className="space-y-3">
                      {signals
                        .filter((s) => s.intentScore >= 80)
                        .slice(0, 4)
                        .map((signal) => (
                          <div
                            key={signal.id}
                            className="flex items-center gap-3 p-3 rounded-lg bg-surface-overlay/30 border border-surface-border/30 hover:border-surface-border transition-all cursor-pointer"
                            onClick={() => setOutreachSignal(signal)}
                          >
                            <div className="w-8 h-8 rounded-full bg-surface-overlay border border-surface-border flex items-center justify-center text-xs font-semibold text-gray-400 flex-shrink-0">
                              {signal.author
                                .replace(/^u\//, "")
                                .replace(/^@/, "")
                                .charAt(0)
                                .toUpperCase()}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm text-gray-200 truncate">
                                {signal.summary}
                              </p>
                              <p className="text-xs text-gray-500">
                                {signal.author} · {signal.platform}
                              </p>
                            </div>
                            <span className="text-sm font-bold text-red-400 flex-shrink-0">
                              {signal.intentScore}
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Signal Feed */}
          {activeTab === "signals" && (
            <div className="space-y-4 animate-fade-in">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-xl font-bold text-white flex items-center gap-2">
                    <Radio className="w-5 h-5 text-brand-400" />
                    Signal Feed
                  </h1>
                  <p className="text-sm text-gray-500 mt-0.5">
                    {filteredSignals.length} signal
                    {filteredSignals.length !== 1 ? "s" : ""} found
                  </p>
                </div>
                <button onClick={handleExportCSV} className="btn-secondary">
                  <Download className="w-4 h-4" />
                  Export
                </button>
              </div>

              <FilterBar
                filters={filters}
                onFilterChange={setFilters}
                allKeywords={allKeywordTexts}
              />

              {visibleSignals.length > 0 ? (
                <>
                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                    {visibleSignals.map((signal) => (
                      <SignalCard
                        key={signal.id}
                        signal={signal}
                        onGenerateOutreach={setOutreachSignal}
                        onToggleSave={handleToggleSave}
                        onMarkContacted={handleMarkContacted}
                      />
                    ))}
                  </div>
                  {visibleCount < displaySignals.length && (
                    <div className="flex justify-center pt-2">
                      <button
                        onClick={() => setVisibleCount((c) => c + 10)}
                        className="btn-secondary"
                      >
                        <ChevronDown className="w-4 h-4" />
                        Load more ({displaySignals.length - visibleCount}{" "}
                        remaining)
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <EmptyState
                  icon={<Inbox className="w-12 h-12 text-gray-700" />}
                  title="No signals match your filters"
                  description="Try adjusting your filters or add more keywords to monitor."
                />
              )}
            </div>
          )}

          {/* Saved Leads */}
          {activeTab === "leads" && (
            <div className="space-y-4 animate-fade-in">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-xl font-bold text-white flex items-center gap-2">
                    <Users className="w-5 h-5 text-brand-400" />
                    Saved Leads
                  </h1>
                  <p className="text-sm text-gray-500 mt-0.5">
                    {leadsSignals.length} lead
                    {leadsSignals.length !== 1 ? "s" : ""} saved
                  </p>
                </div>
                <button
                  onClick={handleExportCSV}
                  className="btn-secondary"
                  disabled={leadsSignals.length === 0}
                >
                  <Download className="w-4 h-4" />
                  Export Leads
                </button>
              </div>

              {leadsSignals.length > 0 ? (
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                  {leadsSignals.map((signal) => (
                    <SignalCard
                      key={signal.id}
                      signal={signal}
                      onGenerateOutreach={setOutreachSignal}
                      onToggleSave={handleToggleSave}
                      onMarkContacted={handleMarkContacted}
                    />
                  ))}
                </div>
              ) : (
                <EmptyState
                  icon={<Users className="w-12 h-12 text-gray-700" />}
                  title="No saved leads yet"
                  description="Save signals from the feed to start building your lead list."
                />
              )}
            </div>
          )}

          {/* Keywords */}
          {activeTab === "keywords" && (
            <div className="animate-fade-in max-w-4xl">
              <KeywordManager
                keywords={keywords}
                onAddKeyword={handleAddKeyword}
                onRemoveKeyword={handleRemoveKeyword}
                onToggleKeyword={handleToggleKeyword}
              />
            </div>
          )}
        </main>
      </div>

      {/* Outreach Modal */}
      {outreachSignal && (
        <OutreachModal
          signal={outreachSignal}
          onClose={() => setOutreachSignal(null)}
        />
      )}

      {/* New Signal Toast */}
      {newSignalToast && (
        <NewSignalToast
          signal={newSignalToast}
          onDismiss={() => setNewSignalToast(null)}
          onView={() => {
            setActiveTab("signals");
            setNewSignalToast(null);
          }}
        />
      )}
    </div>
  );
}

function EmptyState({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      {icon}
      <h3 className="text-lg font-medium text-gray-300 mt-4">{title}</h3>
      <p className="text-sm text-gray-500 mt-1 max-w-md">{description}</p>
    </div>
  );
}
