"""Scrape the public contribution calendar (no token needed)."""
import json, re
import requests
from bs4 import BeautifulSoup

USER = "abhi9rai"
url = f"https://github.com/users/{USER}/contributions"
html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td.ContributionCalendar-day"):
    date = td.get("data-date")
    if not date:
        continue
    tip = tips.get(td.get("id"), "")
    m = re.match(r"(\d+) contribution", tip)
    days.append({"date": date, "level": int(td.get("data-level", 0)),
                 "count": int(m.group(1)) if m else 0})
days.sort(key=lambda d: d["date"])

total = sum(d["count"] for d in days)
best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
cur = 0
for d in reversed(days):
    if d["count"]:
        cur += 1
    elif d is days[-1]:
        continue          # today may still be empty
    else:
        break

json.dump({"user": USER, "days": days, "total": total, "current_streak": cur,
           "longest_streak": longest, "best_day": best}, open("data/contributions.json", "w"), indent=1)
print(f"{len(days)} days, {total} contributions, streak {cur}, longest {longest}")
