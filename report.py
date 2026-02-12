from typing import Dict, List
from collections import Counter


def build_report_md(audit_results: Dict, output_path: str) -> None:
    pages: List[Dict] = audit_results["pages"]
    issues: List[Dict] = audit_results["issues"]

    issue_counts = Counter(issue["issue_type"] for issue in issues)
    sorted_issues = sorted(
        issues, key=lambda item: (item["priority"], item["issue_type"], item["url"])
    )
    top_tasks = sorted_issues[:10]

    lines = []
    lines.append("# SEO Audit Report\n")
    lines.append(f"Total pages crawled: {len(pages)}\n")

    lines.append("## Issue counts by type\n")
    if issue_counts:
        for issue_type, count in issue_counts.most_common():
            lines.append(f"- {issue_type}: {count}")
    else:
        lines.append("- No issues found.")
    lines.append("")

    lines.append("## Top 10 tasks\n")
    if top_tasks:
        for issue in top_tasks:
            lines.append(
                f"- {issue['priority']} {issue['issue_type']} | {issue['url']}"
            )
    else:
        lines.append("- No tasks generated.")
    lines.append("")

    lines.append("## Page summary\n")
    lines.append("| URL | Title | Meta desc length | H1 count | Canonical present |")
    lines.append("| --- | --- | --- | --- | --- |")
    for page in pages:
        title = page["title"].replace("|", " ") if page["title"] else ""
        meta_len = len(page["meta_description"]) if page["meta_description"] else 0
        canonical_present = "yes" if page["canonical"] else "no"
        lines.append(
            f"| {page['url']} | {title} | {meta_len} | {page['h1_count']} | {canonical_present} |"
        )

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
