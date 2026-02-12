from typing import Dict, List
from parser import parse_page_fields


def run_audit(crawl_results: List[Dict]) -> Dict:
    pages: List[Dict] = []
    issues: List[Dict] = []

    for item in crawl_results:
        fields = parse_page_fields(item["url"], item["html"]) if item["html"] else {}
        page = {
            "url": item["url"],
            "status_code": item["status_code"],
            "response_time_ms": item["response_time_ms"],
            "title": fields.get("title", ""),
            "meta_description": fields.get("meta_description", ""),
            "canonical": fields.get("canonical", ""),
            "h1_text": fields.get("h1_text", ""),
            "h1_count": fields.get("h1_count", 0),
            "word_count": fields.get("word_count", 0),
            "internal_links_count": fields.get("internal_links_count", 0),
        }
        pages.append(page)

    title_to_urls: Dict[str, List[str]] = {}
    for page in pages:
        title_key = page["title"].strip().lower()
        if title_key:
            title_to_urls.setdefault(title_key, []).append(page["url"])

    for page in pages:
        url = page["url"]
        status = page["status_code"]
        title = page["title"]
        meta_desc = page["meta_description"]
        h1_count = page["h1_count"]
        canonical = page["canonical"]
        word_count = page["word_count"]

        if status != 200:
            issues.append(
                {
                    "url": url,
                    "issue_type": "status_code_not_200",
                    "priority": "P0",
                    "why_this_matters": "Non-200 pages can hurt indexing and user trust.",
                    "acceptance_criteria": "Page returns HTTP 200 for this URL.",
                }
            )

        if not title:
            issues.append(
                {
                    "url": url,
                    "issue_type": "title_missing",
                    "priority": "P1",
                    "why_this_matters": "Titles help search engines understand pages.",
                    "acceptance_criteria": "A unique title tag exists on the page.",
                }
            )
        elif len(title) < 20:
            issues.append(
                {
                    "url": url,
                    "issue_type": "title_too_short",
                    "priority": "P2",
                    "why_this_matters": "Short titles are less descriptive for users.",
                    "acceptance_criteria": "Title length is at least 20 characters.",
                }
            )

        if not meta_desc:
            issues.append(
                {
                    "url": url,
                    "issue_type": "meta_description_missing",
                    "priority": "P1",
                    "why_this_matters": "Descriptions improve SERP click-through rate.",
                    "acceptance_criteria": "Meta description is present.",
                }
            )
        elif len(meta_desc) < 70:
            issues.append(
                {
                    "url": url,
                    "issue_type": "meta_description_too_short",
                    "priority": "P2",
                    "why_this_matters": "Short descriptions reduce context for users.",
                    "acceptance_criteria": "Meta description length is at least 70 characters.",
                }
            )

        if h1_count == 0:
            issues.append(
                {
                    "url": url,
                    "issue_type": "h1_missing",
                    "priority": "P1",
                    "why_this_matters": "H1 helps signal the primary topic.",
                    "acceptance_criteria": "Page has exactly one H1.",
                }
            )
        elif h1_count > 1:
            issues.append(
                {
                    "url": url,
                    "issue_type": "multiple_h1",
                    "priority": "P2",
                    "why_this_matters": "Multiple H1 tags can dilute topic focus.",
                    "acceptance_criteria": "Page has exactly one H1.",
                }
            )

        if not canonical:
            issues.append(
                {
                    "url": url,
                    "issue_type": "canonical_missing",
                    "priority": "P2",
                    "why_this_matters": "Canonicals help avoid duplicate content issues.",
                    "acceptance_criteria": "Canonical link tag is present.",
                }
            )

        if word_count < 200:
            issues.append(
                {
                    "url": url,
                    "issue_type": "low_content",
                    "priority": "P2",
                    "why_this_matters": "Thin content reduces relevance signals.",
                    "acceptance_criteria": "Page has at least 200 words of text.",
                }
            )

    for title_key, urls in title_to_urls.items():
        if len(urls) > 1:
            for url in urls:
                issues.append(
                    {
                        "url": url,
                        "issue_type": "duplicate_title",
                        "priority": "P2",
                        "why_this_matters": "Duplicate titles can confuse search engines.",
                        "acceptance_criteria": "Title is unique across crawled pages.",
                    }
                )

    return {"pages": pages, "issues": issues}
