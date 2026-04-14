"""Stradvert agency configuration, templates, and constants."""

AGENCY = {
    "name": "Stradvert",
    "founder": "Ryan",
    "website": "streetscaled.com",
    "service": "street interview ads for DTC brands and AI apps",
    "format": "street interview format",
    "differentiator": (
        "Real human reactions that cannot be faked or replicated by AI "
        "or generic UGC creators"
    ),
    "case_study": {
        "client_type": "AI trading platform",
        "format": "street interview ads",
        "result": "£0.86 cost per purchase",
        "benchmark": "£1.54 to £2.48 (UGC benchmark)",
        "saving_pct": "44-65% lower cost per purchase vs UGC",
    },
}

DM_SCRIPTS = [
    {
        "id": 1,
        "label": "Script 1 - Results Without Risk",
        "template": (
            "Hey {firstName}, if I could get you {results} without "
            "{risk}, {call_to_action}?"
        ),
    },
    {
        "id": 2,
        "label": "Script 2 - Vague to Specific",
        "template": (
            "Hey {firstName}, could you handle {vague_result}? "
            "I might be able to get you {specific_result}."
        ),
    },
    {
        "id": 3,
        "label": "Script 3 - Not Sure If You Need It",
        "template": (
            "Hey {firstName}, not sure if you have the need for it "
            "but I could get you {result}. {call_to_action}?"
        ),
    },
    {
        "id": 4,
        "label": "Script 4 - Results + PS Service Line",
        "template": (
            "Hey {firstName}, I can get you {results} without {risk}, "
            "{call_to_action}? ps - we do {service} for {icp} to get "
            "{outcome}."
        ),
    },
    {
        "id": 5,
        "label": "Script 5 - Case Study Lead",
        "template": (
            "Hey {firstName}, we've been working with {case_study} to "
            "get {result}. If we could do that for you {call_to_action}?"
        ),
    },
]

CHANNEL_MESSAGES = [
    {
        "id": 1,
        "channel": "LinkedIn / Email",
        "description": "Professional but casual outreach referencing their ads",
    },
    {
        "id": 2,
        "channel": "Instagram DM",
        "description": "Short, punchy, direct message referencing their content",
    },
    {
        "id": 3,
        "channel": "Follow-Up (any channel)",
        "description": "Bump message sent 2-3 days after no reply, adds new value",
    },
]

TONE_GUIDE = """
Tone rules (STRICT):
- Direct, casual, human. Sound like a real person who actually looked at their ads.
- No corporate language. No em dashes. No exclamation marks unless absolutely natural.
- Short sentences. Conversational.
- Reference something SPECIFIC about their brand, ads, or creative.
- Never sound like a template. Every message should feel hand-typed.
- No filler phrases like "I hope this finds you well" or "I'd love to connect".
- No buzzwords like "synergy", "leverage", "optimize", "scale".
- The pitch is street interview ads as an upgrade to whatever they're doing now.
"""

RESEARCH_PROMPT = """You are a brand research analyst for Stradvert, a creative agency that produces street interview ads for DTC brands and AI apps.

Given the following raw research data about a brand, extract and organize:

1. **Brand Overview**: What they sell, their positioning, price point, target customer
2. **Current Ad Strategy**: What their ads look like based on the research (UGC, studio, influencer, etc.)
3. **Target Customer Profile**: Who buys from them (demographics, psychographics)
4. **Head of Growth / Marketing Contact**: Name and title if found. If not found, note "Not found - check LinkedIn"
5. **Creative Weakness**: The single biggest weakness or gap in their current creative strategy. Be specific. This is what we'll pitch against.
6. **Key Hooks**: 2-3 specific things about the brand we can reference in outreach to show we actually researched them

Be specific and factual. Only state what the research supports. If data is thin, say so.
"""

OUTREACH_PROMPT = """You are Ryan from Stradvert. You write outreach messages for your agency that shoots street interview ads for DTC brands and AI apps.

Your writing style: direct, casual, human. No corporate language. No em dashes. Short sentences. You sound like someone who actually looked at the brand's ads and has a specific take on what they could do better.

Your proof point: you ran street interview ads for an AI trading platform and hit £0.86 cost per purchase. UGC benchmark for the same spend was £1.54 to £2.48. That's real. Use it.

Your differentiator: real human reactions on camera can't be faked by AI or replicated by generic UGC creators. Street interviews feel authentic because they ARE authentic.

IMPORTANT RULES:
- Replace EVERY variable in every script with something real and specific to the brand
- No placeholders left blank. No {brackets} in the output.
- No em dashes (--) anywhere
- No exclamation marks unless completely natural
- Reference specific things about the brand's current ads or creative
- The "risk" variable should be something the brand is currently wasting money on or worried about
- The "result" should be specific to their business (lower CPA, more conversions, better ROAS, etc.)
- Keep it short. These are DMs, not essays.
- Sound like Ryan typed each one by hand after looking at their ads library

TONE GUIDE:
{tone_guide}
"""
