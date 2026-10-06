#!/usr/bin/env python3
"""Refresh profile cards from GitHub's public calendar and user endpoint.

Uses Python's standard library, without a personal access token. A changed or
incomplete upstream response fails loudly, keeping the previous cards intact.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


DEFAULT_USERNAME = "jatinsingh1603"
ROOT = Path(__file__).resolve().parent
HEADERS = {"User-Agent": "Jatin-GitHub-Profile/1.0", "Accept-Language": "en-US"}
MONTHS = {name: index for index, name in enumerate(
    ("January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"), 1)}


class CalendarError(ValueError):
    """GitHub did not return a complete, internally consistent calendar."""


def iso_date(value: str) -> date:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise CalendarError(f"Invalid ISO calendar date: {value!r}")
    return date.fromisoformat(value)


def integer(value: str) -> int:
    if not re.fullmatch(r"(?:0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)", value):
        raise CalendarError(f"Invalid contribution count: {value!r}")
    return int(value.replace(",", ""))


class CalendarParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.cells: list[dict] = []
        self.tooltips: dict[str, str] = {}
        self.bounds: list[tuple[str, str]] = []
        self.summaries: list[str] = []
        self._tooltip: str | None = None
        self._summary = False

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attrs = dict(attrs)
        if "js-calendar-graph" in attrs.get("class", "").split():
            self.bounds.append((attrs.get("data-from", ""), attrs.get("data-to", "")))
        if "ContributionCalendar-day" in attrs.get("class", "").split() and "data-date" in attrs:
            self.cells.append(attrs)
        if tag == "tool-tip" and attrs.get("for"):
            key = attrs["for"]
            if key in self.tooltips:
                raise CalendarError("Duplicate contribution tooltip")
            self._tooltip = key
            self.tooltips[key] = ""
        if attrs.get("id") == "js-contribution-activity-description":
            self._summary = True
            self.summaries.append("")

    def handle_data(self, value: str) -> None:
        if self._tooltip is not None:
            self.tooltips[self._tooltip] += value
        if self._summary:
            self.summaries[-1] += value

    def handle_endtag(self, tag: str) -> None:
        if tag == "tool-tip":
            self._tooltip = None
        if tag == "h2":
            self._summary = False


def parse_calendar(html: str, today: date | None = None) -> dict:
    """Parse every calendar day; never infer missing or malformed values as zero."""
    parser = CalendarParser()
    parser.feed(html)
    parser.close()
    if len(parser.bounds) != 1 or len(parser.summaries) != 1 or not parser.cells:
        raise CalendarError("Missing or ambiguous contribution calendar")
    start_text, end_text = parser.bounds[0]
    start, end = iso_date(start_text[:10]), iso_date(end_text[:10])
    expected_count = (end - start).days + 1
    # The rolling year includes partial boundary weeks, normally 365–371 days.
    if not 360 <= expected_count <= 372:
        raise CalendarError("Unexpected calendar date range")
    if today is not None and end not in {today, today - timedelta(days=1)}:
        raise CalendarError("GitHub returned a stale or future calendar")
    summary = " ".join(parser.summaries[0].split())
    summary_match = re.fullmatch(r"([\d,]+) contributions? in the last year", summary)
    if not summary_match:
        raise CalendarError("Unrecognized contribution summary")
    stated_total = integer(summary_match[1])
    days: dict[str, dict] = {}
    seen_ids: set[str] = set()
    for cell in parser.cells:
        day_text, cell_id = cell["data-date"], cell.get("id", "")
        day = iso_date(day_text)
        if not start <= day <= end or day_text in days:
            raise CalendarError("Duplicate or out-of-range contribution date")
        if not cell_id or cell_id in seen_ids:
            raise CalendarError("Missing or duplicate contribution cell ID")
        seen_ids.add(cell_id)
        tooltip = " ".join(parser.tooltips.get(cell_id, "").split())
        match = re.fullmatch(
            r"(No|[\d,]+) contributions? on ([A-Za-z]+) (\d{1,2})(?:st|nd|rd|th)?(?:, (\d{4}))?\.",
            tooltip,
        )
        if not match:
            raise CalendarError(f"Missing or unrecognized contribution tooltip for {day_text}")
        count = 0 if match[1] == "No" else integer(match[1])
        if MONTHS.get(match[2]) != day.month or int(match[3]) != day.day:
            raise CalendarError(f"Tooltip date does not match {day_text}")
        if match[4] and int(match[4]) != day.year:
            raise CalendarError(f"Tooltip year does not match {day_text}")
        if "data-count" in cell and integer(cell["data-count"]) != count:
            raise CalendarError(f"Conflicting contribution counts for {day_text}")
        level_text = cell.get("data-level", "")
        if level_text not in {"0", "1", "2", "3", "4"}:
            raise CalendarError(f"Invalid contribution level for {day_text}")
        level = int(level_text)
        if (count == 0) != (level == 0):
            raise CalendarError(f"Contribution count/level mismatch for {day_text}")
        days[day_text] = {"date": day_text, "count": count, "level": level}
    expected_dates = {(start + timedelta(days=i)).isoformat() for i in range(expected_count)}
    if set(days) != expected_dates:
        raise CalendarError("Contribution calendar has missing days")
    ordered = [days[key] for key in sorted(days)]
    total = sum(day["count"] for day in ordered)
    if total != stated_total:
        raise CalendarError(f"Calendar sum {total} differs from GitHub summary {stated_total}")
    return {"range_start": start.isoformat(), "range_end": end.isoformat(), "days": ordered, "total": total}


def summarize(days: list[dict], today: date) -> dict:
    """Calculate metrics within the supplied rolling calendar window."""
    if not days:
        raise CalendarError("Cannot summarize an empty calendar")
    counts = {day["date"]: day["count"] for day in days}
    total = sum(counts.values())
    active = sum(count > 0 for count in counts.values())
    longest = running = 0
    month_counts: dict[str, int] = defaultdict(int)
    for day in days:
        running = running + 1 if day["count"] else 0
        longest = max(longest, running)
        month_counts[day["date"][:7]] += day["count"]
    current = 0
    cursor = today
    # Keep yesterday's streak alive while today's contribution count is zero.
    if not counts.get(cursor.isoformat(), 0):
        cursor -= timedelta(days=1)
    while counts.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    best = max(days, key=lambda day: day["count"])
    return {
        "total": total,
        "active_days": active,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best["count"],
        "best_day_date": best["date"],
        "average_active_day": round(total / active, 1) if active else 0.0,
        "months": [{"month": month, "count": count} for month, count in sorted(month_counts.items())],
    }


def fetch_text(url: str) -> str:
    request = Request(url, headers=HEADERS)
    with urlopen(request, timeout=40) as response:
        if response.status != 200:
            raise RuntimeError(f"GitHub returned HTTP {response.status}")
        return response.read(4_000_001).decode("utf-8")


def fetch_data(username: str = DEFAULT_USERNAME, now: datetime | None = None) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", username):
        raise ValueError("Invalid GitHub username")
    now = now or datetime.now(timezone.utc)
    now = now.astimezone(timezone.utc)
    calendar = parse_calendar(fetch_text(f"https://github.com/users/{username}/contributions"), now.date())
    public_user = json.loads(fetch_text(f"https://api.github.com/users/{username}"))
    if public_user.get("login", "").lower() != username.lower():
        raise ValueError("GitHub user response did not match the requested account")
    for field in ("public_repos", "followers"):
        if type(public_user.get(field)) is not int or public_user[field] < 0:
            raise ValueError(f"Missing or invalid public profile field: {field}")
    return {
        "username": username,
        "fetched_at": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        **calendar,
        **summarize(calendar["days"], now.date()),
        "public_repos": public_user["public_repos"],
        "followers": public_user["followers"],
    }


def update(root: Path = ROOT, username: str = DEFAULT_USERNAME) -> dict:
    # Fetch and validate everything before creating or replacing a generated file.
    data = fetch_data(username)
    from render_profile import render

    with tempfile.TemporaryDirectory(prefix=".profile-refresh-", dir=root) as temp:
        staged = Path(temp)
        assets = staged
        render(data, assets)
        for name in ("activity.svg", "stats.svg"):
            if ET.parse(assets / name).getroot().tag != "{http://www.w3.org/2000/svg}svg":
                raise ValueError(f"Renderer did not produce a valid SVG: {name}")
        (staged / "activity.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        for relative in ("activity.json", "activity.svg", "stats.svg"):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged / relative, destination)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    args = parser.parse_args()
    try:
        data = update(username=args.username)
    except Exception as error:
        print(f"Profile refresh failed: {error}", file=sys.stderr)
        return 1
    print(f"Updated @{data['username']}: {data['total']:,} contributions across {len(data['days'])} days.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
