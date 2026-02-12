# Aureate Labs SEO Audit

## How to run

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate`
   - `pip install -r requirements.txt`
2. Run the crawler:
   - `python main.py`
   - Optional: `python main.py --limit 20 --delay-ms 400`

Outputs are written to `outputs/backlog.csv` and `outputs/report.md`.

## Crawling approach

- Breadth-first crawl starting from https://aureatelabs.com.
- Normalizes URLs by stripping query strings and fragments.
- Avoids non-HTML assets by filtering common file extensions and content-type.
- Skips external domains and keeps a visited set to prevent loops.
- Adds a small delay between requests.

## Assumptions and limitations

- Basic HTML parsing only (no JavaScript rendering).
- Word count is an approximation based on visible text extraction.
- Internal link count is a simple count of anchor tags on the page.
- Canonical is read from `link[rel=canonical]` if present.

