"""Claude API integration for brand analysis and outreach generation."""

import logging

import anthropic

from .config import (
    AGENCY,
    DM_SCRIPTS,
    CHANNEL_MESSAGES,
    TONE_GUIDE,
    RESEARCH_PROMPT,
    OUTREACH_PROMPT,
)

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"


def get_client() -> anthropic.Anthropic:
    """Create an Anthropic client (reads ANTHROPIC_API_KEY from env)."""
    return anthropic.Anthropic()


def analyze_brand(research_text: str, brand_name: str) -> str:
    """Analyze raw research data and produce a structured brand brief."""
    client = get_client()

    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": (
                    f"{RESEARCH_PROMPT}\n\n"
                    f"Brand: {brand_name}\n\n"
                    f"Raw Research Data:\n{research_text}"
                ),
            }
        ],
    )

    return message.content[0].text


def generate_outreach(brand_name: str, brand_analysis: str) -> str:
    """Generate all 5 DM scripts + 3 channel messages using Claude."""
    client = get_client()

    # Build the script templates section
    script_section = "DM SCRIPT TEMPLATES TO FILL IN:\n\n"
    for script in DM_SCRIPTS:
        script_section += f"{script['label']}:\n{script['template']}\n\n"

    # Build the channel messages section
    channel_section = "ADDITIONAL CHANNEL-SPECIFIC MESSAGES TO WRITE:\n\n"
    for msg in CHANNEL_MESSAGES:
        channel_section += (
            f"Message {msg['id']} - {msg['channel']}:\n"
            f"{msg['description']}\n\n"
        )

    # Agency context
    agency_context = f"""
AGENCY CONTEXT:
- Agency: {AGENCY['name']}
- Founder: {AGENCY['founder']}
- Website: {AGENCY['website']}
- Service: {AGENCY['service']}
- Format: {AGENCY['format']}
- Differentiator: {AGENCY['differentiator']}
- Case study: {AGENCY['case_study']['client_type']}
- Case study result: {AGENCY['case_study']['result']}
- UGC benchmark: {AGENCY['case_study']['benchmark']}
"""

    prompt = f"""{OUTREACH_PROMPT.format(tone_guide=TONE_GUIDE)}

{agency_context}

BRAND ANALYSIS:
{brand_analysis}

BRAND NAME: {brand_name}

YOUR TASK:
1. Fill in ALL 5 DM scripts below. Replace every single variable with something real and specific to {brand_name}. No placeholders. No brackets. Every variable must be replaced.

{script_section}

2. Write 3 additional outreach messages. Each must reference something specific about the brand's ads or creative strategy. Each pitches street interview format as the upgrade.

{channel_section}

FORMAT YOUR OUTPUT EXACTLY LIKE THIS:

---

DM SCRIPT 1 - Results Without Risk
[Channel: Instagram DM / LinkedIn DM]

[Full message here, no variables, no brackets]

---

DM SCRIPT 2 - Vague to Specific
[Channel: Instagram DM / LinkedIn DM]

[Full message here]

---

(continue for all 5 scripts)

---

LINKEDIN / EMAIL OUTREACH
[Subject line if email]

[Full message here]

---

INSTAGRAM DM

[Full message here]

---

FOLLOW-UP MESSAGE (send 2-3 days after no reply)
[Channel: any]

[Full message here]

---

IMPORTANT: Double check that ZERO variables or brackets remain. Every {{}} must be replaced with real text specific to {brand_name}.
"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return message.content[0].text


def run_analysis_pipeline(
    research_text: str, brand_name: str
) -> tuple[str, str]:
    """Run the full analysis pipeline: analyze brand, then generate outreach.

    Returns (brand_analysis, outreach_messages).
    """
    logger.info("Analyzing brand: %s", brand_name)
    brand_analysis = analyze_brand(research_text, brand_name)

    logger.info("Generating outreach messages for: %s", brand_name)
    outreach = generate_outreach(brand_name, brand_analysis)

    return brand_analysis, outreach
