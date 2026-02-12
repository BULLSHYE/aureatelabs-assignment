import argparse
from crawler import crawl_site
from auditor import run_audit
from backlog import build_backlog_csv
from report import build_report_md
from utils.url_utils import normalize_seed_url


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a limited SEO crawl.")
    parser.add_argument("--limit", type=int, default=25, help="Max pages to crawl")
    parser.add_argument(
        "--seed",
        type=str,
        default="https://aureatelabs.com",
        # help="Seed URL to start crawling",
    )
    parser.add_argument(
        "--delay-ms", type=int, default=350, help="Delay between requests"
    )
    args = parser.parse_args()

    seed_url = normalize_seed_url(args.seed)
    crawl_results = crawl_site(seed_url, limit=args.limit, delay_ms=args.delay_ms)
    audit_results = run_audit(crawl_results)
    build_backlog_csv(audit_results, "outputs/backlog.csv")
    build_report_md(audit_results, "outputs/report.md")


if __name__ == "__main__":
    main()
