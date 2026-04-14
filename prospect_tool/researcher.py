"""Web research module - scrapes brand websites and searches for ad/marketing info."""

import re
import time
import logging
from urllib.parse import urlparse, quote_plus

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

REQUEST_TIMEOUT = 20


def _retry_request(url: str, max_retries: int = 2) -> requests.Response | None:
    """Make a GET request with retry logic."""
    for attempt in range(max_retries + 1):
        try:
            resp = requests.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True
            )
            resp.raise_for_status()
            return resp
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code in (429, 503):
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
            raise
        except requests.exceptions.ConnectionError:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            raise
    return None


def scrape_website(url: str) -> dict:
    """Scrape a brand's website for key information."""
    if not url.startswith("http"):
        url = f"https://{url}"

    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "headings": [],
        "body_text": "",
        "links": [],
        "error": None,
    }

    try:
        resp = _retry_request(url)
        if resp is None:
            result["error"] = "Failed after retries"
            return result

        soup = BeautifulSoup(resp.text, "html.parser")

        # Title
        if soup.title:
            result["title"] = soup.title.get_text(strip=True)

        # Meta description
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            result["meta_description"] = meta["content"]

        # OG description fallback
        if not result["meta_description"]:
            og = soup.find("meta", attrs={"property": "og:description"})
            if og and og.get("content"):
                result["meta_description"] = og["content"]

        # Headings
        for tag in ["h1", "h2", "h3"]:
            for h in soup.find_all(tag, limit=10):
                text = h.get_text(strip=True)
                if text:
                    result["headings"].append(f"[{tag}] {text}")

        # Body text (clean)
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        body_text = soup.get_text(separator=" ", strip=True)
        body_text = re.sub(r"\s+", " ", body_text)
        result["body_text"] = body_text[:5000]

        # Navigation / key links
        for a in soup.find_all("a", href=True, limit=30):
            href = a["href"]
            text = a.get_text(strip=True)
            if text and len(text) < 100:
                result["links"].append(f"{text} -> {href}")

    except Exception as e:
        result["error"] = str(e)
        logger.warning("Failed to scrape %s: %s", url, e)

    return result


def _search_ddg(query: str, max_results: int = 8) -> list[dict]:
    """Search using ddgs library (or legacy duckduckgo_search)."""
    results = []
    try:
        # Try the newer ddgs package first
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })
    except Exception as e:
        logger.debug("DDGS library search failed: %s", e)
    return results


def _search_html(query: str, max_results: int = 8) -> list[dict]:
    """Fallback search by scraping DuckDuckGo HTML."""
    results = []
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.find_all("div", class_="result", limit=max_results):
            title_el = item.find("a", class_="result__a")
            snippet_el = item.find("a", class_="result__snippet")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "url": title_el.get("href", ""),
                    "snippet": (
                        snippet_el.get_text(strip=True) if snippet_el else ""
                    ),
                })
    except Exception as e:
        logger.debug("HTML search fallback failed: %s", e)
    return results


def search_web(query: str, max_results: int = 8) -> list[dict]:
    """Search the web with automatic fallback between methods."""
    # Try the DDGS library first
    results = _search_ddg(query, max_results)
    if results:
        return results

    # Fallback to HTML scraping
    logger.info("Using HTML search fallback for: %s", query)
    results = _search_html(query, max_results)
    if results:
        return results

    logger.warning("All search methods failed for: %s", query)
    return []


def search_ads_library(brand_name: str) -> list[dict]:
    """Search for a brand's ads on Facebook Ad Library and other sources."""
    queries = [
        f"{brand_name} facebook ads library",
        f"{brand_name} ads creative examples",
        f"{brand_name} advertising strategy",
        f"{brand_name} UGC ads",
    ]
    all_results = []
    for q in queries:
        all_results.extend(search_web(q, max_results=4))
        time.sleep(0.5)  # rate limit protection
    return all_results


def find_marketing_contact(brand_name: str) -> list[dict]:
    """Search for head of growth / marketing contact at the brand."""
    queries = [
        f"{brand_name} head of growth LinkedIn",
        f"{brand_name} head of marketing LinkedIn",
        f"{brand_name} VP marketing",
        f"{brand_name} CMO",
        f"{brand_name} growth lead",
    ]
    all_results = []
    for q in queries:
        all_results.extend(search_web(q, max_results=3))
        time.sleep(0.5)
    return all_results


def research_brand(brand_name: str, website: str) -> dict:
    """Run the full research pipeline for a brand.

    Returns a dict with all raw research data ready for analysis.
    """
    logger.info("Researching %s (%s)...", brand_name, website)

    parsed = urlparse(website if "://" in website else f"https://{website}")
    domain = parsed.netloc or parsed.path.split("/")[0]

    # 1. Scrape main site
    site_data = scrape_website(website)

    # 2. Try to scrape about page
    about_data = scrape_website(f"https://{domain}/about")

    # 3. General brand search
    brand_search = search_web(f"{brand_name} brand what do they sell", max_results=8)
    time.sleep(0.5)

    # 4. Product / customer search
    product_search = search_web(
        f"{brand_name} reviews target customer demographics",
        max_results=6,
    )
    time.sleep(0.5)

    # 5. Ad library / creative search
    ads_search = search_ads_library(brand_name)

    # 6. Marketing contact search
    contact_search = find_marketing_contact(brand_name)

    # 7. Competitor / industry context
    industry_search = search_web(
        f"{brand_name} competitors market industry",
        max_results=4,
    )

    return {
        "brand_name": brand_name,
        "website": website,
        "site_data": site_data,
        "about_data": about_data,
        "brand_search": brand_search,
        "product_search": product_search,
        "ads_search": ads_search,
        "contact_search": contact_search,
        "industry_search": industry_search,
    }


def format_research_for_prompt(research: dict) -> str:
    """Format all raw research into a readable block for the AI prompt."""
    sections = []

    # Site data
    site = research["site_data"]
    sections.append("=== WEBSITE DATA ===")
    sections.append(f"URL: {site['url']}")
    sections.append(f"Title: {site['title']}")
    sections.append(f"Meta: {site['meta_description']}")
    if site["headings"]:
        sections.append("Headings: " + " | ".join(site["headings"][:15]))
    if site["body_text"]:
        sections.append(f"Body excerpt: {site['body_text'][:3000]}")
    if site["error"]:
        sections.append(f"Scrape error: {site['error']}")

    # About page
    about = research["about_data"]
    if about["body_text"] and not about["error"]:
        sections.append("\n=== ABOUT PAGE ===")
        sections.append(f"Body: {about['body_text'][:2000]}")

    # Brand search results
    sections.append("\n=== BRAND SEARCH RESULTS ===")
    for r in research["brand_search"]:
        sections.append(f"- {r['title']}: {r['snippet']}")

    # Product / customer search
    sections.append("\n=== PRODUCT & CUSTOMER SEARCH ===")
    for r in research["product_search"]:
        sections.append(f"- {r['title']}: {r['snippet']}")

    # Ads search
    sections.append("\n=== ADS & CREATIVE SEARCH ===")
    for r in research["ads_search"]:
        sections.append(f"- {r['title']}: {r['snippet']}")

    # Contact search
    sections.append("\n=== MARKETING CONTACT SEARCH ===")
    for r in research["contact_search"]:
        sections.append(f"- {r['title']}: {r['snippet']}")

    # Industry context
    sections.append("\n=== INDUSTRY & COMPETITORS ===")
    for r in research["industry_search"]:
        sections.append(f"- {r['title']}: {r['snippet']}")

    return "\n".join(sections)
