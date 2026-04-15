import { Signal, Keyword } from "./types";

const twitterSignals: Signal[] = [
  {
    id: "tw-001",
    platform: "twitter",
    author: "Sarah Chen",
    authorHandle: "@sarahchen_mktg",
    authorAvatar: "",
    content:
      "Looking for an AI tool that can help automate our social media posting. We're a team of 5 and manually scheduling everything is killing our productivity. Anyone recommend something that's not too expensive?",
    url: "https://twitter.com/sarahchen_mktg/status/1234567890",
    timestamp: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    intentScore: 92,
    urgency: "high",
    keywords: ["AI tools", "social media", "automation"],
    summary:
      "Marketing team lead actively seeking affordable AI social media automation tool for small team.",
    status: "new",
  },
  {
    id: "tw-002",
    platform: "twitter",
    author: "Marcus Rivera",
    authorHandle: "@marcusrivera",
    authorAvatar: "",
    content:
      "Need help with our dentist marketing. We've tried Facebook ads but the ROI is terrible. Looking for someone who specializes in dental practice marketing. Budget is there, just need results.",
    url: "https://twitter.com/marcusrivera/status/1234567891",
    timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
    intentScore: 95,
    urgency: "high",
    keywords: ["dentist marketing", "Facebook ads", "dental practice"],
    summary:
      "Dentist seeking specialized marketing help. Has budget, frustrated with current Facebook ad results.",
    status: "new",
  },
  {
    id: "tw-003",
    platform: "twitter",
    author: "Dev Patel",
    authorHandle: "@devpatel_saas",
    authorAvatar: "",
    content:
      "Anyone using a good CRM for SaaS startups? We've outgrown our spreadsheet and need something that integrates with Stripe. Open to suggestions!",
    url: "https://twitter.com/devpatel_saas/status/1234567892",
    timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
    intentScore: 78,
    urgency: "medium",
    keywords: ["CRM", "SaaS", "Stripe integration"],
    summary:
      "SaaS founder looking for CRM with Stripe integration, outgrowing current solution.",
    status: "new",
  },
  {
    id: "tw-004",
    platform: "twitter",
    author: "Jenny Park",
    authorHandle: "@jennypark_co",
    authorAvatar: "",
    content:
      "Frustrated with our current email marketing platform. Deliverability has tanked and support is non-existent. Looking for alternatives that actually work for e-commerce. Any suggestions?",
    url: "https://twitter.com/jennypark_co/status/1234567893",
    timestamp: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
    intentScore: 88,
    urgency: "high",
    keywords: ["email marketing", "e-commerce", "deliverability"],
    summary:
      "E-commerce business owner frustrated with email platform, actively seeking replacement.",
    status: "new",
  },
  {
    id: "tw-005",
    platform: "twitter",
    author: "Tom Nguyen",
    authorHandle: "@tomnguyen_tech",
    authorAvatar: "",
    content:
      "Thinking about trying some new project management tools. Our team is getting bigger and Notion alone isn't cutting it anymore. Not urgent but would love recs.",
    url: "https://twitter.com/tomnguyen_tech/status/1234567894",
    timestamp: new Date(Date.now() - 1000 * 60 * 300).toISOString(),
    intentScore: 52,
    urgency: "low",
    keywords: ["project management", "team tools"],
    summary:
      "Tech lead casually exploring project management alternatives to Notion for growing team.",
    status: "new",
  },
];

const redditSignals: Signal[] = [
  {
    id: "rd-001",
    platform: "reddit",
    author: "u/startup_founder_23",
    authorHandle: "u/startup_founder_23",
    authorAvatar: "",
    content:
      "We just closed our seed round and need to set up proper analytics. Currently flying blind with no tracking. What are the best analytics platforms for a B2B SaaS? Budget isn't a concern, we need something robust.",
    url: "https://reddit.com/r/SaaS/comments/abc123",
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    intentScore: 91,
    urgency: "high",
    keywords: ["analytics", "B2B SaaS", "tracking"],
    summary:
      "Funded startup founder urgently needs analytics platform. Has budget, needs robust B2B solution.",
    status: "new",
    subreddit: "r/SaaS",
  },
  {
    id: "rd-002",
    platform: "reddit",
    author: "u/agency_owner_mike",
    authorHandle: "u/agency_owner_mike",
    authorAvatar: "",
    content:
      "Running a marketing agency and we need better client reporting. Currently spending 10+ hours a week manually building reports. Need something that pulls from Google Ads, Meta, and GA4 automatically. Willing to pay premium for something that saves us time.",
    url: "https://reddit.com/r/Marketing/comments/def456",
    timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    intentScore: 89,
    urgency: "high",
    keywords: ["marketing agency", "client reporting", "automation"],
    summary:
      "Agency owner spending 10+ hrs/week on reports, willing to pay premium for automated reporting tool.",
    status: "new",
    subreddit: "r/Marketing",
  },
  {
    id: "rd-003",
    platform: "reddit",
    author: "u/ecom_emily",
    authorHandle: "u/ecom_emily",
    authorAvatar: "",
    content:
      "Has anyone tried using AI for customer support? We get about 200 tickets/day and our team can't keep up. Looking for something that can handle basic questions automatically but still feels human. Currently on Zendesk.",
    url: "https://reddit.com/r/Entrepreneur/comments/ghi789",
    timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
    intentScore: 85,
    urgency: "high",
    keywords: ["AI", "customer support", "automation", "Zendesk"],
    summary:
      "E-commerce operator overwhelmed with 200 daily tickets, seeking AI customer support solution.",
    status: "new",
    subreddit: "r/Entrepreneur",
  },
  {
    id: "rd-004",
    platform: "reddit",
    author: "u/freelance_dev_mark",
    authorHandle: "u/freelance_dev_mark",
    authorAvatar: "",
    content:
      "What's the best invoicing software for freelancers? I've been using Wave but it's getting clunky. Need something that handles multiple currencies and has good recurring invoice support.",
    url: "https://reddit.com/r/Entrepreneur/comments/jkl012",
    timestamp: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
    intentScore: 68,
    urgency: "medium",
    keywords: ["invoicing", "freelancer", "billing"],
    summary:
      "Freelancer looking to switch invoicing tools, needs multi-currency and recurring billing.",
    status: "new",
    subreddit: "r/Entrepreneur",
  },
  {
    id: "rd-005",
    platform: "reddit",
    author: "u/local_biz_owner",
    authorHandle: "u/local_biz_owner",
    authorAvatar: "",
    content:
      "Anyone recommend a good website builder for a small restaurant? Don't need anything fancy, just a menu, hours, location, and online ordering. Tried Wix but it felt overwhelming.",
    url: "https://reddit.com/r/smallbusiness/comments/mno345",
    timestamp: new Date(Date.now() - 1000 * 60 * 360).toISOString(),
    intentScore: 61,
    urgency: "medium",
    keywords: ["website builder", "restaurant", "small business"],
    summary:
      "Restaurant owner seeking simple website builder with online ordering. Found Wix too complex.",
    status: "new",
    subreddit: "r/smallbusiness",
  },
];

const linkedinSignals: Signal[] = [
  {
    id: "li-001",
    platform: "linkedin",
    author: "Amanda Foster",
    authorHandle: "amanda-foster-cmo",
    authorAvatar: "",
    content:
      "We're scaling our content team from 3 to 10 people this quarter. Looking for a content management and workflow platform that can handle editorial calendars, approvals, and multi-channel publishing. If you've used something great, I'd love to hear about it. DMs open!",
    url: "https://linkedin.com/posts/amanda-foster-cmo_content-scaling",
    timestamp: new Date(Date.now() - 1000 * 60 * 20).toISOString(),
    intentScore: 87,
    urgency: "high",
    keywords: ["content management", "workflow", "scaling team"],
    summary:
      "CMO tripling content team, actively seeking content workflow platform. DMs open.",
    status: "new",
  },
  {
    id: "li-002",
    platform: "linkedin",
    author: "Robert Kim",
    authorHandle: "robert-kim-ceo",
    authorAvatar: "",
    content:
      "Just had our quarterly planning and realized we need to get serious about lead generation. Our outbound is basically non-existent. Anyone recommend good B2B lead gen tools or agencies? Particularly interested in LinkedIn outreach automation.",
    url: "https://linkedin.com/posts/robert-kim-ceo_lead-gen",
    timestamp: new Date(Date.now() - 1000 * 60 * 75).toISOString(),
    intentScore: 90,
    urgency: "high",
    keywords: ["lead generation", "B2B", "LinkedIn outreach", "outbound"],
    summary:
      "CEO acknowledging need for outbound lead gen after quarterly planning. Open to tools and agencies.",
    status: "new",
  },
  {
    id: "li-003",
    platform: "linkedin",
    author: "Diana Martinez",
    authorHandle: "diana-martinez-hr",
    authorAvatar: "",
    content:
      "Our hiring process is a mess. We're using 4 different tools and nothing talks to each other. Need a proper ATS that integrates with LinkedIn and our HRIS. Any HR tech folks have suggestions?",
    url: "https://linkedin.com/posts/diana-martinez-hr_ats-search",
    timestamp: new Date(Date.now() - 1000 * 60 * 150).toISOString(),
    intentScore: 82,
    urgency: "high",
    keywords: ["ATS", "HR tech", "hiring", "integration"],
    summary:
      "HR director frustrated with fragmented hiring stack, seeking integrated ATS solution.",
    status: "new",
  },
  {
    id: "li-004",
    platform: "linkedin",
    author: "James Wright",
    authorHandle: "james-wright-ops",
    authorAvatar: "",
    content:
      "Curious about what others are using for internal documentation. We've tried Confluence and it's... not great. Would love something more modern and actually enjoyable to use. Open to suggestions.",
    url: "https://linkedin.com/posts/james-wright-ops_docs",
    timestamp: new Date(Date.now() - 1000 * 60 * 400).toISOString(),
    intentScore: 55,
    urgency: "low",
    keywords: ["documentation", "knowledge base", "internal tools"],
    summary:
      "Ops lead casually exploring Confluence alternatives for internal documentation.",
    status: "new",
  },
  {
    id: "li-005",
    platform: "linkedin",
    author: "Priya Sharma",
    authorHandle: "priya-sharma-growth",
    authorAvatar: "",
    content:
      "We need to revamp our entire onboarding flow. Current activation rate is 12% and it's killing our growth. Looking for a product-led growth consultant or tool that can help us improve time-to-value. Budget approved, need to move fast.",
    url: "https://linkedin.com/posts/priya-sharma-growth_onboarding",
    timestamp: new Date(Date.now() - 1000 * 60 * 50).toISOString(),
    intentScore: 96,
    urgency: "high",
    keywords: ["onboarding", "product-led growth", "activation", "consulting"],
    summary:
      "Growth lead with approved budget urgently seeking PLG consultant/tool. 12% activation rate crisis.",
    status: "new",
  },
];

export const allSignals: Signal[] = [
  ...twitterSignals,
  ...redditSignals,
  ...linkedinSignals,
].sort(
  (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
);

export const defaultKeywords: Keyword[] = [
  {
    id: "kw-1",
    text: "AI tools",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-2",
    text: "dentist marketing",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-3",
    text: "SaaS",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-4",
    text: "lead generation",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-5",
    text: "automation",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-6",
    text: "email marketing",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-7",
    text: "CRM",
    isActive: false,
    createdAt: new Date().toISOString(),
  },
  {
    id: "kw-8",
    text: "customer support",
    isActive: true,
    createdAt: new Date().toISOString(),
  },
];

// Generate a new simulated signal for real-time updates
const newSignalTemplates = [
  {
    platform: "twitter" as const,
    author: "Alex Thompson",
    authorHandle: "@alexthompson_biz",
    content:
      "Desperately need a better accounting solution for our startup. QuickBooks is driving me insane. Anyone using something modern that actually works with multiple entities?",
    keywords: ["accounting", "startup", "QuickBooks alternative"],
    summary:
      "Startup founder frustrated with QuickBooks, urgently seeking modern multi-entity accounting.",
    intentScore: 86,
    urgency: "high" as const,
  },
  {
    platform: "reddit" as const,
    author: "u/growth_hacker_99",
    authorHandle: "u/growth_hacker_99",
    content:
      "Looking for an SEO tool that doesn't cost $400/month. Ahrefs and SEMrush are overkill for what we need. Just want keyword tracking and basic site audit. Any budget-friendly options?",
    keywords: ["SEO", "keyword tracking", "budget tools"],
    summary:
      "Growth marketer seeking affordable SEO tool alternative to Ahrefs/SEMrush.",
    intentScore: 72,
    urgency: "medium" as const,
    subreddit: "r/Marketing",
  },
  {
    platform: "linkedin" as const,
    author: "Michelle Lee",
    authorHandle: "michelle-lee-vp",
    content:
      "Our team is drowning in Slack notifications. We need a better async communication tool that reduces noise but keeps everyone aligned. Currently evaluating options. Thoughts?",
    keywords: ["async communication", "team tools", "Slack alternative"],
    summary:
      "VP evaluating async communication tools to replace Slack. Team productivity suffering.",
    intentScore: 74,
    urgency: "medium" as const,
  },
  {
    platform: "twitter" as const,
    author: "Carlos Diaz",
    authorHandle: "@carlosdiaz_ecom",
    content:
      "Need a Shopify expert ASAP. Our conversion rate dropped 40% after a theme update and we can't figure out why. Willing to pay premium for someone who can fix this today.",
    keywords: ["Shopify", "e-commerce", "conversion rate"],
    summary:
      "E-commerce owner with urgent Shopify conversion crisis. Ready to pay premium for immediate help.",
    intentScore: 97,
    urgency: "high" as const,
  },
  {
    platform: "reddit" as const,
    author: "u/startup_cto",
    authorHandle: "u/startup_cto",
    content:
      "We're migrating from AWS to something more cost-effective. Our bill went from $2k to $8k/month and we're barely scaling. Anyone have experience with Railway, Render, or Fly.io for production workloads?",
    keywords: ["cloud hosting", "AWS alternative", "infrastructure"],
    summary:
      "CTO dealing with 4x AWS cost increase, actively evaluating cloud alternatives for production.",
    intentScore: 83,
    urgency: "high" as const,
    subreddit: "r/SaaS",
  },
];

let newSignalIndex = 0;

export function generateNewSignal(): Signal {
  const template = newSignalTemplates[newSignalIndex % newSignalTemplates.length];
  newSignalIndex++;
  return {
    ...template,
    id: `new-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    authorAvatar: "",
    url: `https://${template.platform}.com/post/${Date.now()}`,
    timestamp: new Date().toISOString(),
    status: "new",
  };
}
