"""Document output module - generates clean .docx and .txt files for VA use."""

import os
import re
import logging
from datetime import datetime

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def sanitize_filename(name: str) -> str:
    """Make a brand name safe for use as a filename."""
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def generate_txt(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> str:
    """Generate a clean .txt file with all outreach content.

    Returns the path to the created file.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    ensure_output_dir()

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(brand_name)
    filename = f"{safe_name}_outreach_{date_str}.txt"
    filepath = os.path.join(output_dir, filename)

    lines = []
    lines.append("=" * 70)
    lines.append(f"STRADVERT OUTREACH PACK - {brand_name.upper()}")
    lines.append(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("")

    # Brand analysis section
    lines.append("-" * 70)
    lines.append("BRAND RESEARCH BRIEF")
    lines.append("-" * 70)
    lines.append("")
    lines.append(brand_analysis)
    lines.append("")
    lines.append("")

    # Outreach messages section
    lines.append("-" * 70)
    lines.append("OUTREACH MESSAGES - READY TO COPY & SEND")
    lines.append("-" * 70)
    lines.append("")
    lines.append(outreach_messages)
    lines.append("")
    lines.append("")

    # Footer
    lines.append("=" * 70)
    lines.append("END OF OUTREACH PACK")
    lines.append(f"Agency: Stradvert | streetscaled.com")
    lines.append("=" * 70)

    content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("Created TXT: %s", filepath)
    return filepath


def generate_docx(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> str:
    """Generate a clean .docx file with all outreach content.

    Returns the path to the created file.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    ensure_output_dir()

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(brand_name)
    filename = f"{safe_name}_outreach_{date_str}.docx"
    filepath = os.path.join(output_dir, filename)

    doc = Document()

    # Set default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Arial"
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Title
    title = doc.add_heading(f"Stradvert Outreach Pack", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Subtitle with brand name and date
    subtitle = doc.add_paragraph()
    run = subtitle.add_run(f"{brand_name}")
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    subtitle.add_run(
        f"\nGenerated: {datetime.now().strftime('%B %d, %Y')}"
    ).font.size = Pt(10)

    doc.add_paragraph("")  # spacer

    # Brand Research Brief
    doc.add_heading("Brand Research Brief", level=1)

    # Split analysis into paragraphs and add them
    for block in brand_analysis.split("\n\n"):
        block = block.strip()
        if not block:
            continue

        # Check if it's a heading (starts with ** or #)
        if block.startswith("**") and block.endswith("**"):
            heading_text = block.strip("*").strip()
            doc.add_heading(heading_text, level=2)
        elif block.startswith("#"):
            heading_text = block.lstrip("#").strip()
            doc.add_heading(heading_text, level=2)
        else:
            # Handle bold markers within text
            p = doc.add_paragraph()
            parts = re.split(r"(\*\*.*?\*\*)", block)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    run = p.add_run(part.strip("*"))
                    run.bold = True
                else:
                    p.add_run(part)

    doc.add_page_break()

    # Outreach Messages
    doc.add_heading("Outreach Messages - Ready to Copy & Send", level=1)

    instruction = doc.add_paragraph()
    run = instruction.add_run(
        "Copy each message exactly as written. Do not edit. "
        "Each message is ready to send."
    )
    run.italic = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph("")  # spacer

    # Split outreach into sections by --- dividers
    sections = re.split(r"\n---+\n", outreach_messages)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split("\n")
        first_line = lines[0].strip()

        # Check if first line is a heading
        if (
            first_line.upper().startswith("DM SCRIPT")
            or first_line.upper().startswith("LINKEDIN")
            or first_line.upper().startswith("INSTAGRAM")
            or first_line.upper().startswith("FOLLOW")
            or first_line.upper().startswith("EMAIL")
        ):
            doc.add_heading(first_line, level=2)
            message_body = "\n".join(lines[1:]).strip()
        else:
            message_body = section

        if message_body:
            # Add the message in a slightly indented, distinct style
            for para_text in message_body.split("\n\n"):
                para_text = para_text.strip()
                if not para_text:
                    continue

                # Channel label lines
                if para_text.startswith("[") and para_text.endswith("]"):
                    p = doc.add_paragraph()
                    run = p.add_run(para_text)
                    run.italic = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
                else:
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Inches(0.25)
                    # Handle any remaining bold markers
                    parts = re.split(r"(\*\*.*?\*\*)", para_text)
                    for part in parts:
                        if part.startswith("**") and part.endswith("**"):
                            run = p.add_run(part.strip("*"))
                            run.bold = True
                        else:
                            p.add_run(part)

        # Add a line break between sections
        doc.add_paragraph("")

    # Footer
    footer_para = doc.add_paragraph()
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_para.add_run("Stradvert | streetscaled.com")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

    doc.save(filepath)
    logger.info("Created DOCX: %s", filepath)
    return filepath


def generate_all(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> dict:
    """Generate both .txt and .docx output files.

    Returns dict with paths to both files.
    """
    txt_path = generate_txt(brand_name, brand_analysis, outreach_messages, output_dir)
    docx_path = generate_docx(
        brand_name, brand_analysis, outreach_messages, output_dir
    )

    return {
        "txt": txt_path,
        "docx": docx_path,
    }
