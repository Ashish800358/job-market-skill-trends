# scraper/remoteok_scraper.py
import argparse
import time
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import os
from scraper.base import BaseScraper

REMOTEOK_URL = "https://remoteok.com/remote-{}-jobs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobTrendsBot/1.0; +https://github.com/yourname)"
}

class RemoteOKScraper(BaseScraper):
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except Exception:
            return None

    def _extract_desc_from_detail(self, url: str) -> str:
        """Fetch a job's detail page and return best-effort text."""
        soup = self._fetch_page(url)
        if not soup:
            return ""
        # Try a few likely containers in case RemoteOK’s HTML shifts
        candidates = [
            "div.description",            # common
            "div#job > div > div",        # fallback
            "section",                    # broad fallback
            "article"
        ]
        for sel in candidates:
            el = soup.select_one(sel)
            if el and el.get_text(strip=True):
                return el.get_text(" ", strip=True)
        return ""

    def search(self, role: str, location: str, limit: int = 100) -> List[Dict[str, str]]:
        role_slug = "-".join(role.lower().split())
        url = REMOTEOK_URL.format(role_slug)

        soup = self._fetch_page(url)
        if not soup:
            return []

        jobs = []
        for row in soup.select("tr.job"):
            title_el = row.select_one("h2")
            company_el = row.select_one("h3")
            link_el = row.select_one("a.preventLink")

            title = title_el.get_text(strip=True) if title_el else ""
            company = company_el.get_text(strip=True) if company_el else ""
            url_path = link_el.get("href") if link_el else ""
            job_url = f"https://remoteok.com{url_path}" if url_path and url_path.startswith("/") else url_path

            desc = ""
            if job_url:
                # polite pause to avoid hammering
                time.sleep(0.5)
                desc = self._extract_desc_from_detail(job_url)

            if title:
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": "Remote",
                    "url": job_url or url,
                    "description": desc
                })
            if len(jobs) >= limit:
                break
        return jobs


def write_latest_copy(path: str) -> None:
    latest = "data/raw/latest.csv"
    try:
        import shutil
        shutil.copy2(path, latest)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, help='e.g. "data analyst"')
    parser.add_argument("--location", default="remote")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    scraper = RemoteOKScraper()
    print(f"[scraper] fetching RemoteOK jobs for role='{args.role}' ...")
    rows = scraper.search(args.role, args.location, args.limit)

    out_path = scraper.default_output_path()
    scraper.save_csv(rows, out_path)
    write_latest_copy(out_path)
    print(f"[scraper] wrote {len(rows)} rows to: {out_path}")
    print("[scraper] also updated: data/raw/latest.csv")


if __name__ == "__main__":
    # ensure pkg import works if run directly
    if __package__ is None and not os.path.exists("scraper/__init__.py"):
        open("scraper/__init__.py", "a").close()
    main()
