from typing import Dict
from bs4 import BeautifulSoup
from utils.url_utils import is_internal_url, normalize_url


def parse_page_fields(url: str, html: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""

    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag.get("content").strip()

    canonical = ""
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag and canonical_tag.get("href"):
        canonical = canonical_tag.get("href").strip()

    h1_tags = soup.find_all("h1")
    h1_text = h1_tags[0].get_text(strip=True) if h1_tags else ""

    text = soup.get_text(" ", strip=True)
    words = [w for w in text.split() if w]
    word_count = len(words)

    internal_links = 0
    for link in soup.find_all("a", href=True):
        normalized = normalize_url(url, link.get("href"))
        if normalized and is_internal_url(url, normalized):
            internal_links += 1

    return {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "canonical": canonical,
        "h1_text": h1_text,
        "h1_count": len(h1_tags),
        "word_count": word_count,
        "internal_links_count": internal_links,
    }
