"""CLI interface for the Stradvert Prospect Research & Outreach Generator."""

import argparse
import logging
import sys
import os

from dotenv import load_dotenv

from .researcher import research_brand, format_research_for_prompt
from .analyzer import run_analysis_pipeline
from .output import generate_all


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def print_banner():
    """Print the Stradvert tool banner."""
    print()
    print("=" * 58)
    print("  STRADVERT - AI Prospect Research & Outreach Generator")
    print("  streetscaled.com")
    print("=" * 58)
    print()


def run_for_brand(brand_name: str, website: str, output_dir: str = None):
    """Run the full pipeline for a single brand."""
    logger = logging.getLogger(__name__)

    print(f"  Brand:   {brand_name}")
    print(f"  Website: {website}")
    print()

    # Step 1: Research
    print("[1/4] Researching brand...")
    research = research_brand(brand_name, website)
    research_text = format_research_for_prompt(research)
    logger.debug("Research text length: %d chars", len(research_text))
    print("       Done. Collected data from website + web search.")

    # Step 2: Analyze
    print("[2/4] Analyzing brand and identifying creative weaknesses...")
    brand_analysis, outreach_messages = run_analysis_pipeline(
        research_text, brand_name
    )
    print("       Done. Brand brief and weakness identified.")

    # Step 3: Generate outreach
    print("[3/4] Outreach messages generated (5 DM scripts + 3 channel messages).")

    # Step 4: Output documents
    print("[4/4] Creating output documents...")
    paths = generate_all(brand_name, brand_analysis, outreach_messages, output_dir)
    print("       Done.")

    print()
    print("-" * 58)
    print("  OUTPUT FILES:")
    print(f"  TXT:  {paths['txt']}")
    print(f"  DOCX: {paths['docx']}")
    print("-" * 58)
    print()
    print("  Your VA can open either file, copy, and send.")
    print("  No editing needed. All messages are ready to go.")
    print()

    return paths


def interactive_mode(output_dir: str = None):
    """Run in interactive mode - keep accepting brands until user quits."""
    print("Interactive mode. Type 'quit' or 'q' to exit.")
    print()

    while True:
        try:
            brand_name = input("Brand name (or 'q' to quit): ").strip()
            if brand_name.lower() in ("q", "quit", "exit"):
                print("Done.")
                break
            if not brand_name:
                continue

            website = input("Website URL: ").strip()
            if not website:
                print("Website is required. Try again.")
                continue

            print()
            run_for_brand(brand_name, website, output_dir)

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"\nError processing brand: {e}")
            logging.getLogger(__name__).exception("Pipeline error")
            print("Try another brand or check the error above.\n")


def main():
    """Main entry point."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Stradvert AI Prospect Research & Outreach Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single brand
  python -m prospect_tool --brand "Huel" --website "huel.com"

  # Interactive mode (process multiple brands)
  python -m prospect_tool --interactive

  # Custom output directory
  python -m prospect_tool --brand "AG1" --website "drinkag1.com" --output ./my_output
        """,
    )

    parser.add_argument(
        "--brand", "-b",
        type=str,
        help="Brand name to research",
    )
    parser.add_argument(
        "--website", "-w",
        type=str,
        help="Brand website URL",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output directory (default: ./output)",
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode (process multiple brands)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose/debug logging",
    )

    args = parser.parse_args()

    setup_logging(args.verbose)
    print_banner()

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        print("Set it in your .env file or export it:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        print()
        sys.exit(1)

    if args.interactive:
        interactive_mode(args.output)
    elif args.brand and args.website:
        run_for_brand(args.brand, args.website, args.output)
    else:
        print("Usage: Provide --brand and --website, or use --interactive mode.")
        print()
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
