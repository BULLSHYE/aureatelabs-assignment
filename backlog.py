import csv
from typing import Dict


def build_backlog_csv(audit_results: Dict, output_path: str) -> None:
    issues = audit_results["issues"]
    priority_rank = {"P0": 0, "P1": 1, "P2": 2}
    issues = sorted(
        issues,
        key=lambda issue: (
            priority_rank.get(issue.get("priority", "P2"), 3),
            issue.get("url", ""),
            issue.get("issue_type", ""),
        ),
    )
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "task_id",
                "url",
                "issue_type",
                "priority",
                "why_this_matters",
                "acceptance_criteria",
            ],
        )
        writer.writeheader()
        for idx, issue in enumerate(issues, start=1):
            row = {"task_id": f"TASK-{idx:03d}", **issue}
            writer.writerow(row)
