#!/usr/bin/env python3
"""Refresh GitHub profile artwork using public data and Python's standard library.

Run: python3 scripts/update_profile.py
Re-render without network: python3 scripts/update_profile.py --offline
"""

import argparse
from collections import Counter
from datetime import date, datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from profile_artwork import architecture, divider, footer, header, project_card, stack, svg
from work_atlas import build_atlas

USER = "arpitkjaiswal"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
COLORS = ["#86f7cf", "#b5a0ff", "#e8bc85", "#7ab7ef", "#e99ab7", "#a5d68b", "#63c8c8", "#c7bbec", "#f0d88b"]


def fetch(url):
    request = Request(url, headers={"User-Agent": "ArpitProfileArtwork/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


class RepositoryParser(HTMLParser):
    """Read repository cards, preserving fork status and primary language."""

    def __init__(self):
        super().__init__()
        self.repos = []
        self.depth = 0
        self.repo = None
        self.text = []
        self.language = False
        self.next_page = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("rel") == "next":
            self.next_page = True
        if tag == "li" and attrs.get("itemprop") == "owns":
            self.depth = 1
            self.repo = {"name": "", "language": None, "fork": False}
            self.text = []
        elif tag == "li" and self.depth:
            self.depth += 1
        if self.depth:
            if tag == "a" and attrs.get("itemprop") == "name codeRepository":
                self.repo["name"] = attrs["href"].strip("/").split("/")[-1]
            if attrs.get("itemprop") == "programmingLanguage":
                self.language = True

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)
            if self.language and data.strip():
                self.repo["language"] = data.strip()

    def handle_endtag(self, tag):
        if tag == "span":
            self.language = False
        if tag == "li" and self.depth:
            self.depth -= 1
            if not self.depth:
                if not self.repo["name"]:
                    raise ValueError("Repository markup changed: name was not found")
                self.repo["fork"] = "Forked from" in " ".join(self.text)
                self.repos.append(self.repo)


class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tooltips = {}
        self.tooltip_id = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-date" in attrs and "data-level" in attrs:
            self.cells[attrs["id"]] = {
                "date": attrs["data-date"], "level": int(attrs["data-level"])
            }
        if tag == "tool-tip":
            self.tooltip_id = attrs.get("for")
            self.text = []

    def handle_data(self, data):
        if self.tooltip_id:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.tooltip_id:
            text = "".join(self.text).strip()
            match = re.match(r"([\d,]+) contributions? on ", text)
            if match:
                self.tooltips[self.tooltip_id] = int(match[1].replace(",", ""))
            elif text.startswith("No contributions on "):
                self.tooltips[self.tooltip_id] = 0
            self.tooltip_id = None

    def days(self):
        if len(self.cells) < 300:
            raise ValueError("Incomplete contribution calendar; keeping the existing artwork")
        days = []
        for key, cell in self.cells.items():
            if key not in self.tooltips:
                raise ValueError(f"Contribution count missing for {cell['date']}")
            days.append({**cell, "count": self.tooltips[key]})
        return sorted(days, key=lambda day: day["date"])


def collect():
    repos = []
    for page in range(1, 21):
        parser = RepositoryParser()
        parser.feed(fetch(f"https://github.com/{USER}?page={page}&tab=repositories"))
        if not parser.repos:
            raise ValueError(f"No repository cards on page {page}; refusing partial data")
        repos.extend(parser.repos)
        if not parser.next_page:
            break
    else:
        raise ValueError("Repository pagination exceeded the safety limit")
    if len({repo["name"] for repo in repos}) != len(repos):
        raise ValueError("Duplicate repository cards; refusing inconsistent data")
    contributions = ContributionParser()
    contributions.feed(fetch(f"https://github.com/users/{USER}/contributions"))
    return {
        "user": USER,
        "updated": datetime.now(timezone.utc).date().isoformat(),
        "sources": [f"https://github.com/{USER}?page=1&tab=repositories",
                    f"https://github.com/users/{USER}/contributions"],
        "repositories": repos,
        "contributions": contributions.days(),
    }


def languages(data):
    own = [r for r in data["repositories"] if not r["fork"] and r["name"] != USER]
    counts = Counter(r["language"] for r in own if r["language"])
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    total = sum(counts.values())
    if not total:
        raise ValueError("No primary languages found; repository markup may have changed")
    content = [f'<text x="32" y="42" font-size="20" font-weight="700">Repository language mix</text>',
               f'<text x="32" y="68" font-size="12" class="muted">{total} non-fork projects with a detected primary language</text>']
    offset = 0
    for i, (language, count) in enumerate(ordered):
        color = COLORS[i % len(COLORS)]
        part = count / total * 100
        content.append(f'<circle cx="134" cy="181" r="73" fill="none" stroke="{color}" stroke-width="22" pathLength="100" stroke-dasharray="{part:.4f} {100-part:.4f}" stroke-dashoffset="{-offset:.4f}" transform="rotate(-90 134 181)"/>')
        y = 106 + i * 22
        content.append(f'<circle cx="258" cy="{y-4}" r="4" fill="{color}"/><text x="272" y="{y}" font-size="13">{escape(language)}</text><text x="548" y="{y}" text-anchor="end" font-size="13" class="mono">{count} · {part:.0f}%</text>')
        offset += part
    content.extend([
        f'<text x="134" y="181" text-anchor="middle" font-size="34" font-weight="800">{total}</text>',
        '<text x="134" y="204" text-anchor="middle" font-size="12" class="muted">PROJECTS</text>',
        '<circle class="motion" cx="134" cy="181" r="92" fill="none" stroke="#86f7cf" opacity=".35" stroke-dasharray="5 12"><animateTransform attributeName="transform" type="rotate" from="0 134 181" to="360 134 181" dur="60s" repeatCount="indefinite"/></circle>',
        f'<text x="32" y="{max(318, 108+22*len(ordered))}" font-size="11" class="muted">One primary language per project · not code volume · {data["updated"]}</text>',
    ])
    return svg(580, max(348, 138+22*len(ordered)), "Project language distribution",
               "; ".join(f"{lang}: {count} projects" for lang, count in ordered), "\n".join(content))


def calendar(data):
    days = data["contributions"]
    first = date.fromisoformat(days[0]["date"])
    active = sum(day["count"] > 0 for day in days)
    total = sum(day["count"] for day in days)
    palette = ["#17212b", "#204c43", "#337b65", "#59ba92", "#86f7cf"]
    content = [
        '<text x="32" y="42" font-size="20" font-weight="700">Contribution history</text>',
        f'<text x="32" y="69" font-size="13" class="muted">{total:,} contributions · {active} active days · GitHub public calendar</text>',
    ]
    positions = []
    months = set()
    for day in days:
        current = date.fromisoformat(day["date"])
        delta = (current - first).days + (first.weekday()+1) % 7
        col, row = divmod(delta, 7)
        x, y = 52 + col * 20, 116 + row * 20
        color = palette[day["level"]]
        content.append(f'<rect x="{x}" y="{y}" width="15" height="15" rx="3" fill="{color}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
        positions.append((x+7.5, y+7.5))
        month = (current.year, current.month)
        if month not in months and (not months or current.day == 1):
            months.add(month)
            content.append(f'<text x="{x}" y="103" font-size="11" class="muted">{current:%b}</text>')
    path = "M" + " L".join(f"{x},{y}" for x, y in positions)
    content.append(f'<circle class="motion" r="4" fill="#fff" opacity=".85"><animateMotion path="{path}" dur="55s" repeatCount="indefinite"/></circle>')
    for row, label in [(1, "M"), (3, "W"), (5, "F")]:
        content.append(f'<text x="28" y="{127+row*20}" font-size="10" class="muted">{label}</text>')
    content.append(f'<text x="32" y="290" font-size="11" class="muted">{days[0]["date"]} → {days[-1]["date"]} · updated {data["updated"]} UTC</text>')
    content.append('<text x="990" y="290" font-size="10" class="muted">LESS</text>')
    for i, color in enumerate(palette):
        content.append(f'<rect x="{1022+i*18}" y="279" width="12" height="12" rx="2" fill="{color}"/>')
    content.append('<text x="1118" y="290" font-size="10" class="muted">MORE</text>')
    return svg(1200, 320, "Animated GitHub contribution calendar",
               f"{total} contributions across {active} active days. The moving light is decorative; each cell shows real GitHub contribution data.", "\n".join(content))


def monthly(data):
    counts = Counter()
    for day in data["contributions"]:
        counts[day["date"][:7]] += day["count"]
    months = sorted(counts)[-12:]
    maximum = max(max(counts.values()), 1)
    content = [
        '<text x="32" y="42" font-size="20" font-weight="700">Monthly contributions</text>',
        '<text x="32" y="68" font-size="12" class="muted">GitHub contributions by month · current month is partial</text>',
    ]
    for tick in range(4):
        y = 260-tick*50
        content.append(f'<path d="M48 {y}H548" stroke="#1b2942" stroke-dasharray="3 6"/>')
        content.append(f'<text x="40" y="{y+4}" text-anchor="end" font-size="9" class="muted">{maximum*tick/3:.0f}</text>')
    for i, month in enumerate(months):
        x = 56 + i * 41
        height = counts[month] / maximum * 150
        y = 260-height
        content.append(f'<rect x="{x}" y="{y:.2f}" width="23" height="{height:.2f}" rx="4" fill="url(#accent)"><title>{month}: {counts[month]} contributions</title></rect>')
        if counts[month]:
            content.append(f'<text x="{x+11.5}" y="{y-8:.2f}" text-anchor="middle" font-size="10" class="mono">{counts[month]}</text>')
        label = date.fromisoformat(month+"-01").strftime("%b")
        content.append(f'<text x="{x+11.5}" y="280" text-anchor="middle" font-size="10" class="muted">{label}</text>')
    content.append('<path d="M48 260H548" stroke="#475569"/>')
    content.append(f'<text x="32" y="318" font-size="11" class="muted">{months[0]} → {months[-1]} · updated {data["updated"]} UTC</text>')
    return svg(580, 348, "Monthly GitHub contributions",
               "; ".join(f"{month}: {counts[month]}" for month in months), "\n".join(content))


def load_profile_data(offline=False, allow_cached=False):
    snapshot = ASSETS / "profile-data.json"
    if offline:
        return json.loads(snapshot.read_text()), False
    try:
        return collect(), True
    except HTTPError as error:
        # Scheduled artwork generation may use already-verified metadata during
        # upstream outages. Authentication and other permanent failures still fail.
        if not allow_cached or error.code not in {429, 500, 502, 503, 504} or not snapshot.exists():
            raise
        cached = json.loads(snapshot.read_text())
        print(f"::warning title=GitHub metadata unavailable::HTTP {error.code}. "
              f"Using saved snapshot dated {cached['updated']} UTC; graph data has not been refreshed.")
        return cached, False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Render the saved snapshot without fetching")
    parser.add_argument("--allow-cached", action="store_true",
                        help="Warn and retain the dated snapshot during transient GitHub HTTP failures")
    args = parser.parse_args()
    snapshot = ASSETS / "profile-data.json"
    data, fresh = load_profile_data(args.offline, args.allow_cached)
    # Render everything before writing, so parsing failures preserve the previous graphs.
    artwork = {"header.svg": header(), "divider.svg": divider(),
               "languages.svg": languages(data), "contributions.svg": calendar(data),
               "monthly.svg": monthly(data), "architecture.svg": architecture(),
               "stack.svg": stack(), "footer.svg": footer(),
               **{f"project-{name}.svg": project_card(name)
                  for name in ("nexora", "talentos", "aegisvault")}}
    artwork.update(build_atlas(data))
    ASSETS.mkdir(exist_ok=True)
    for name, source in artwork.items():
        (ASSETS / name).write_text(source)
    if fresh:
        snapshot.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Rendered {len(artwork)} profile assets from {len(data['repositories'])} repositories and {len(data['contributions'])} calendar days ({data['updated']}).")


if __name__ == "__main__":
    main()
