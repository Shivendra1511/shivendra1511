"""Scrape the public contribution calendar (no token needed) -> data/contributions.json"""
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import GITHUB_USER

OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch_days(user):
    r = requests.get(f"https://github.com/users/{user}/contributions",
                     headers={"User-Agent": "Mozilla/5.0 profile-readme-bot"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td[data-date]"):
        text = tips.get(td.get("id"), "")
        m = re.match(r"(\d+)\s+contribution", text)
        count = int(m.group(1)) if m else 0
        days.append({"date": td["data-date"], "count": count, "level": int(td.get("data-level", 0))})
    days.sort(key=lambda d: d["date"])
    if not days:
        raise SystemExit(f"No contribution cells found for '{user}' - check GITHUB_USER in scripts/config.py")
    return days


def streaks(days):
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)
    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif d["date"] == date.today().isoformat():
            continue            # today may not have contributions yet
        else:
            break
    return current, longest


def main():
    days = fetch_days(GITHUB_USER)
    current, longest = streaks(days)
    months = {}
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]
    best = max(days, key=lambda d: d["count"])
    data = {"user": GITHUB_USER, "generated": datetime.now(timezone.utc).isoformat(),
            "total": sum(d["count"] for d in days), "current_streak": current,
            "longest_streak": longest, "best_day": best, "monthly": months, "days": days}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"{data['total']} contributions, {len(days)} days, streak {current}/{longest}")


if __name__ == "__main__":
    main()
