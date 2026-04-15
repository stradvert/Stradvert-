import { Signal, Outreach, Tone } from "./types";

export function generateOutreach(
  signal: Signal,
  tone: Tone = "professional"
): Outreach {
  const firstName = signal.author.split(" ")[0].replace(/^u\//, "").replace(/^@/, "");
  const isReddit = signal.platform === "reddit";
  const isTwitter = signal.platform === "twitter";
  const isLinkedIn = signal.platform === "linkedin";

  const toneMap = {
    casual: {
      greeting: `Hey ${firstName}!`,
      opener: "Saw your post and had to reach out",
      closer: "Happy to chat more if you're interested!",
      sign: "Cheers",
    },
    professional: {
      greeting: `Hi ${firstName},`,
      opener: "I came across your recent post and it resonated with me",
      closer:
        "I'd love to schedule a quick call to discuss how we might help.",
      sign: "Best regards",
    },
    friendly: {
      greeting: `Hey ${firstName}! 👋`,
      opener: "Your post really caught my eye",
      closer: "Would love to connect and share some ideas!",
      sign: "Talk soon",
    },
  };

  const t = toneMap[tone];
  const painPoint = extractPainPoint(signal.content);
  const solution = suggestSolution(signal.keywords);

  const coldDM = generateColdDM(signal, t, painPoint, solution);
  const email = generateEmail(signal, t, painPoint, solution);
  const publicReply = generatePublicReply(signal, t, painPoint, solution, {
    isReddit,
    isTwitter,
    isLinkedIn,
  });
  const contentIdea = generateContentIdea(signal, painPoint);

  return { coldDM, email, publicReply, contentIdea };
}

function extractPainPoint(content: string): string {
  const painPhrases = [
    { pattern: /frustrated with/i, extract: "frustration with current tools" },
    { pattern: /can't keep up/i, extract: "scaling challenges" },
    { pattern: /killing our/i, extract: "productivity drain" },
    { pattern: /driving me insane/i, extract: "tool frustration" },
    { pattern: /dropped \d+%/i, extract: "performance decline" },
    { pattern: /cost.*\$/i, extract: "cost concerns" },
    { pattern: /too expensive/i, extract: "budget constraints" },
    { pattern: /not.*great/i, extract: "dissatisfaction with current solution" },
    { pattern: /need help/i, extract: "seeking expert guidance" },
    { pattern: /looking for/i, extract: "active solution search" },
    { pattern: /anyone recommend/i, extract: "seeking recommendations" },
    { pattern: /overwhelm/i, extract: "feeling overwhelmed" },
    { pattern: /mess/i, extract: "process disorganization" },
    { pattern: /budget/i, extract: "budget-conscious decision" },
  ];

  for (const { pattern, extract } of painPhrases) {
    if (pattern.test(content)) return extract;
  }
  return "looking for a better solution";
}

function suggestSolution(keywords: string[]): string {
  const solutions: Record<string, string> = {
    "AI tools": "AI-powered automation platform",
    "social media": "social media management suite",
    automation: "workflow automation solution",
    CRM: "modern CRM platform",
    "email marketing": "email marketing platform",
    analytics: "analytics and tracking solution",
    "lead generation": "lead generation engine",
    "customer support": "AI customer support platform",
    invoicing: "invoicing and billing platform",
    "website builder": "website building platform",
    "content management": "content workflow platform",
    ATS: "applicant tracking system",
    documentation: "knowledge management platform",
    onboarding: "user onboarding platform",
    SEO: "SEO optimization toolkit",
    accounting: "modern accounting platform",
    "dentist marketing": "dental practice marketing solution",
    Shopify: "e-commerce optimization service",
    "cloud hosting": "cloud infrastructure platform",
  };

  for (const kw of keywords) {
    for (const [key, solution] of Object.entries(solutions)) {
      if (kw.toLowerCase().includes(key.toLowerCase())) return solution;
    }
  }
  return "purpose-built solution";
}

function generateColdDM(
  signal: Signal,
  t: { greeting: string; opener: string; closer: string; sign: string },
  painPoint: string,
  solution: string
): string {
  return `${t.greeting}

${t.opener} about ${painPoint}. I totally get how that can slow things down.

We've been working on a ${solution} that specifically addresses this — and we've helped similar ${signal.platform === "reddit" ? "communities" : "teams"} see real results within the first week.

A few things that might be relevant to your situation:
• Solves the exact problem you described
• Quick setup (most teams are live in under a day)
• Integrates with tools you're already using

${t.closer}

${t.sign}`;
}

function generateEmail(
  signal: Signal,
  t: { greeting: string; opener: string; closer: string; sign: string },
  painPoint: string,
  solution: string
): string {
  const firstName = signal.author.split(" ")[0].replace(/^u\//, "").replace(/^@/, "");
  return `Subject: Quick thought on your ${painPoint}

${t.greeting}

${t.opener}, and I wanted to share something that might help.

The challenge you described — ${painPoint} — is something we hear about often. It's usually a sign that the current approach has hit its ceiling, and there's a huge opportunity to level up.

We built our ${solution} specifically for situations like yours. Here's what makes it different:

1. **Fast implementation** — Most teams are up and running within 24 hours
2. **Built for your use case** — Not a generic tool trying to do everything
3. **Proven results** — Teams similar to yours typically see 3-5x improvement

I'd love to show you a quick 15-minute demo tailored to your specific needs. No pressure, no hard sell — just want to see if it's a fit.

Would any time this week work for a quick chat?

${t.sign},
[Your Name]

P.S. I noticed you mentioned ${signal.keywords[0]} — we recently published a case study on exactly this topic. Happy to share if you're interested.`;
}

function generatePublicReply(
  signal: Signal,
  t: { greeting: string; opener: string; closer: string; sign: string },
  painPoint: string,
  solution: string,
  platform: { isReddit: boolean; isTwitter: boolean; isLinkedIn: boolean }
): string {
  if (platform.isTwitter) {
    return `Great question! We've seen a lot of teams dealing with ${painPoint} lately.

A few things that helped our clients:
→ Start with a clear requirements list
→ Look for tools with ${signal.keywords[0]} built-in
→ Don't underestimate onboarding support

Happy to share what's worked — DMs are open! 🧵`;
  }

  if (platform.isReddit) {
    return `This is a really common challenge, and I've seen it come up a lot in this sub.

Based on what you're describing (${painPoint}), here are a few things worth considering:

1. **Define your must-haves vs nice-to-haves** — it'll save you time evaluating
2. **Look for ${signal.keywords[0]} integration** — this is usually the make-or-break feature
3. **Ask for a trial or pilot** — don't commit until you've tested with real data

We've helped a few folks in similar situations and I'd be happy to share more details via DM if you're interested. No sales pitch, just genuine advice from someone who's been in the space.`;
  }

  // LinkedIn
  return `${signal.author}, thanks for sharing this — it's a challenge I hear about constantly in conversations with ${signal.keywords[0]} leaders.

A few thoughts from what we've seen work:

✅ Start with the workflow, not the tool — map your process first
✅ Prioritize ${signal.keywords[0]} capabilities — this usually has the biggest ROI
✅ Look for platforms that grow with you — your needs in 6 months will be different

Would love to connect and share some specific insights from teams in similar situations. Feel free to reach out!`;
}

function generateContentIdea(signal: Signal, painPoint: string): string {
  const keyword = signal.keywords[0];
  return `🎯 **Content Angle: "${painPoint}" — A Growing Trend**

**Tweet/Thread idea:**
"Most teams struggling with ${keyword} are making the same 3 mistakes. Here's what we've learned from helping 100+ teams fix this → [thread]"

**Thread structure:**
1. Hook: The real cost of ${painPoint} ($$$ and time)
2. Mistake #1: Choosing tools before defining the workflow
3. Mistake #2: Ignoring integration requirements
4. Mistake #3: Not measuring ROI from day one
5. The framework that actually works (step-by-step)
6. CTA: Free resource/template

**Video angle (60-90s):**
"POV: You just realized your ${keyword} setup is costing you $X/month in lost productivity. Here's the 3-step fix that our clients use..."

**Blog/Newsletter:**
"The ${keyword} Stack in 2025: What's Working, What's Not, and What to Buy"
— Use the original post as a real-world example (anonymized) of a common pain point, then provide actionable advice.`;
}
