export type Platform = "twitter" | "reddit" | "linkedin";
export type Urgency = "low" | "medium" | "high";
export type Tone = "casual" | "professional" | "friendly";
export type LeadStatus = "new" | "saved" | "contacted" | "converted";

export interface Signal {
  id: string;
  platform: Platform;
  author: string;
  authorHandle: string;
  authorAvatar: string;
  content: string;
  url: string;
  timestamp: string;
  intentScore: number;
  urgency: Urgency;
  keywords: string[];
  summary: string;
  status: LeadStatus;
  subreddit?: string;
}

export interface Outreach {
  coldDM: string;
  email: string;
  publicReply: string;
  contentIdea: string;
}

export interface Keyword {
  id: string;
  text: string;
  isActive: boolean;
  createdAt: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface FilterState {
  platform: Platform | "all";
  keyword: string;
  intentLevel: "all" | "high" | "medium" | "low";
  status: LeadStatus | "all";
  search: string;
}

export interface DashboardStats {
  totalSignals: number;
  highIntent: number;
  savedLeads: number;
  contacted: number;
}
