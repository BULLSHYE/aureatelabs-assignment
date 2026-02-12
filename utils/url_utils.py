from typing import Optional
from urllib.parse import urljoin, urlparse, urlunparse

ALLOWED_SCHEMES = {"http", "https"}

ASSET_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".webp",
    ".pdf",
    ".css",
    ".js",
    ".ico",
    ".zip",
    ".mp4",
    ".mov",
    ".avi",
    ".webm",
    ".mp3",
    ".wav",
}


def normalize_seed_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        return "https://" + url
    return url


def strip_fragment_and_query(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
    ).rstrip("/") or url


def normalize_url(base_url: str, href: str) -> Optional[str]:
    if href.startswith("mailto:") or href.startswith("tel:"):
        return None
    joined = urljoin(base_url, href)
    parsed = urlparse(joined)
    if parsed.scheme not in ALLOWED_SCHEMES:
        return None
    normalized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
    )
    return normalized.rstrip("/") or normalized


def is_internal_url(seed_url: str, target_url: str) -> bool:
    seed = urlparse(seed_url)
    target = urlparse(target_url)
    return seed.netloc == target.netloc


def is_html_like(value) -> bool:
    if isinstance(value, str):
        lower = value.lower()
        for ext in ASSET_EXTENSIONS:
            if lower.endswith(ext):
                return False
        return True
    content_type = value.headers.get("Content-Type", "").lower()
    return "text/html" in content_type
