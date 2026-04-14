#!/usr/bin/env python3
"""Stradvert AI Prospect Research & Outreach Generator.

Usage:
    # Single brand
    python main.py --brand "Huel" --website "huel.com"

    # Interactive mode
    python main.py --interactive

    # Or run as module
    python -m prospect_tool --brand "Huel" --website "huel.com"
"""

from prospect_tool.cli import main

if __name__ == "__main__":
    main()
