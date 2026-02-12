import time
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from utils.url_utils import (
    is_html_like,
    is_internal_url,
    normalize_url,
    strip_fragment_and_query,
)

REQUEST_HEADERS = {
    "User-Agent": "SEO-Audit-Bot/1.0 (+https://aureatelabs.com)"
}


def crawl_site(seed_url: str, limit: int = 25, delay_ms: int = 350) -> List[Dict]:
    visited = set()
    queue = [seed_url]
    results: List[Dict] = []

    while queue and len(results) < limit:
        current = queue.pop(0)
        current = strip_fragment_and_query(current)
        if current in visited:
            continue
        visited.add(current)

        start = time.perf_counter()
        try:
            response = requests.get(current, headers=REQUEST_HEADERS, timeout=15)
            status_code = response.status_code
            html = response.text if is_html_like(response) else ""
        except requests.RequestException:
            status_code = 0
            html = ""
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        results.append(
            {
                "url": current,
                "status_code": status_code,
                "response_time_ms": elapsed_ms,
                "html": html,
            }
        )
        print(f"Crawled: {current} (Status: {status_code}, Time: {elapsed_ms}ms), {len(results)}/{limit } pages found")
        if html:
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link.get("href")
                normalized = normalize_url(current, href)
                if not normalized:
                    continue
                normalized = strip_fragment_and_query(normalized)
                if not is_internal_url(seed_url, normalized):
                    continue
                if not is_html_like(normalized):
                    continue
                if normalized not in visited and normalized not in queue:
                    queue.append(normalized)

        time.sleep(delay_ms / 1000.0)

    return results
