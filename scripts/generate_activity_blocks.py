#!/usr/bin/env python3
import os
import sys
import textwrap
import datetime as dt
from collections import defaultdict

import requests

GITHUB_GRAPHQL = "https://api.github.com/graphql"


def get_token():
    """Get GitHub token from env."""
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GH_TOKEN or GITHUB_TOKEN is required", file=sys.stderr)
        sys.exit(1)
    return token


def get_username():
    """Get username from env, fallback to repository owner."""
    return (
        os.getenv("GITHUB_USERNAME")
        or os.getenv("GITHUB_ACTOR")
        or "h4m1dr"
    )


def run_graphql_query(query: str, variables: dict, token: str) -> dict:
    """Send a GraphQL request to GitHub."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    resp = requests.post(
        GITHUB_GRAPHQL,
        json={"query": query, "variables": variables},
        headers=headers,
        timeout=30,
    )
    if resp.status_code != 200:
        print("GraphQL error:", resp.status_code, resp.text, file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    if "errors" in data:
        print("GraphQL returned errors:", data["errors"], file=sys.stderr)
        sys.exit(1)
    return data["data"]


def fetch_daily_contributions(username: str, token: str):
    """Fetch daily contributions for the last 365 days."""
    today = dt.date.today()
    one_year_ago = today - dt.timedelta(days=365)

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    vars_ = {
        "login": username,
        "from": one_year_ago.isoformat() + "T00:00:00Z",
        "to": (today + dt.timedelta(days=1)).isoformat() + "T00:00:00Z",
    }

    data = run_graphql_query(query, vars_, token)
    weeks = (
        data["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    )

    daily = {}  # date_str -> count
    for week in weeks:
        for d in week["contributionDays"]:
            date_str = d["date"][:10]
            daily[date_str] = d["contributionCount"]

    return daily


def make_bar(value: int, max_value: int, width: int = 30) -> str:
    """Return a bar made of unicode blocks."""
    if max_value <= 0:
        max_value = 1
    filled = int(round((value / max_value) * width))
    filled = min(filled, width)
    return "█" * filled + "░" * (width - filled)


def build_weekly_block(daily: dict) -> str:
    """Build the weekly text block (last 7 days)."""
    today = dt.date.today()
    last_7 = []
    for i in range(6, -1, -1):  # 6..0 (oldest -> newest)
        d = today - dt.timedelta(days=i)
        date_str = d.isoformat()
        count = daily.get(date_str, 0)
        last_7.append((d, count))

    max_count = max((c for _, c in last_7), default=1)

    lines = ["Weekly GitHub Activity (contributions)"]
    for d, count in last_7:
        day_name = d.strftime("%a")  # Mon, Tue, ...
        bar = make_bar(count, max_count)
        # Align: e.g. "Thu 7  | "
        lines.append(f"{day_name} {count:<2} | {bar}")
    return "\n".join(lines)


def build_monthly_block(daily: dict) -> str:
    """Build the monthly text block (last 12 months)."""
    today = dt.date.today()
    # aggregate by (year, month)
    monthly_counts = defaultdict(int)
    for date_str, count in daily.items():
        d = dt.date.fromisoformat(date_str)
        key = (d.year, d.month)
        monthly_counts[key] += count

    # last 12 months including current
    months = []
    year = today.year
    month = today.month
    for _ in range(12):
        months.append((year, month))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    months = list(reversed(months))  # oldest -> newest

    max_count = max((monthly_counts[m] for m in months), default=1)

    lines = ["Monthly GitHub Activity (last 12 months)"]
    for (year, month) in months:
        label = dt.date(year, month, 1).strftime("%b %Y")  # Jan 2025
        count = monthly_counts[(year, month)]
        bar = make_bar(count, max_count)
        lines.append(f"{label:<9} | {bar} {count}")
    return "\n".join(lines)


def replace_block(content: str, marker_start: str, marker_end: str, new_block: str):
    """Replace the text between two markers with a code block containing new_block."""
    start_idx = content.find(marker_start)
    end_idx = content.find(marker_end)
    if start_idx == -1 or end_idx == -1:
        raise RuntimeError(f"Markers {marker_start} / {marker_end} not found in README")

    before = content[: start_idx + len(marker_start)]
    after = content[end_idx:]

    wrapped = "\n```text\n" + new_block + "\n```\n"
    return before + wrapped + after


def main():
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")

    token = get_token()
    username = get_username()

    daily = fetch_daily_contributions(username, token)

    weekly_block = build_weekly_block(daily)
    monthly_block = build_monthly_block(daily)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(
        content,
        "<!--START_WEEKLY_ACTIVITY-->",
        "<!--END_WEEKLY_ACTIVITY-->",
        weekly_block,
    )
    content = replace_block(
        content,
        "<!--START_MONTHLY_ACTIVITY-->",
        "<!--END_MONTHLY_ACTIVITY-->",
        monthly_block,
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated README with weekly & monthly GitHub activity")


if __name__ == "__main__":
    main()