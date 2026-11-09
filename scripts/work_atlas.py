"""Build an animated repository network and an offline interactive explorer.

Language links use the GitHub snapshot. Tool links are curated from project
manifests/READMEs reviewed during profile setup; they are not repo dependencies.
"""

from html import escape
import json
import math
from pathlib import Path

from profile_artwork import svg

GROUPS = [
    ("ai", "AI & DATA", "#b5a0ff"),
    ("tools", "TOOLS & WORKSPACES", "#86f7cf"),
    ("backend", "BACKEND & SECURITY", "#e8bc85"),
    ("web", "WEB EXPERIMENTS", "#7ab7ef"),
    ("foundations", "CS & COURSEWORK", "#e99ab7"),
    ("other", "OTHER EXPLORATIONS", "#a5d68b"),
]
AREAS = {
    "ai": ["Candidate-Ranking-System", "AI_Candidate_Ranking_System", "DocumentAnalyser",
           "CNN", "LEXA", "TerraMind", "NovaFlow-AI", "Hypermart-Sales-Data-Analysis-Report-",
           "Data_Analytic_miniproject"],
    "tools": ["NEXORA", "DevOS-AI-Software-Engineering-Agent", "CommitSync", "CommitFlow", "Concord"],
    "backend": ["AegisVault", "veildb", "URLShortener", "URL-Shortener", "Node.js-Express.js"],
    "web": ["arpitkjaiswal.github.io", "Plugin", "orbit-warden", "React-Framework", "js",
            "Amazon-Web-Services", "Javascript"],
    "foundations": ["IS_LAB", "leetcode-solutions", "ESLAB", "neetcode-submissions", "DBS_Lab",
                    "Hotel-management-Application", "hotel-management-system", "Os_Lab",
                    "OSDL_Lab_Project", "OSDL", "DBS", "OOPs_Reopo", "LabcodesDS", "DCCN",
                    "Verilog_codes", "DSA", "OOPS"],
}
ALIASES = {
    "DevOS-AI-Software-Engineering-Agent": "DevOS",
    "Candidate-Ranking-System": "TalentOS",
    "AI_Candidate_Ranking_System": "AI Candidate Ranking",
    "CNN": "LeafScan / CNN",
    "Hypermart-Sales-Data-Analysis-Report-": "Hypermart Sales Analysis",
    "Data_Analytic_miniproject": "Data Analytics Mini-project",
    "Hotel-management-Application": "Hotel Management App",
    "hotel-management-system": "Hotel Management System",
    "arpitkjaiswal.github.io": "Personal Website",
}
# Evidence is deliberately specific. Unreviewed repositories get their primary
# language link, but no inferred framework links based on a name or a fork.
TOOLS = {
    "NEXORA": ["React", "Vite", "Node.js", "Docker", "Playwright"],
    "Candidate-Ranking-System": ["React", "Vite", "FastAPI", "SQLAlchemy", "Alembic", "PostgreSQL", "scikit-learn", "Docker", "pytest"],
    "AI_Candidate_Ranking_System": ["FastAPI", "SQLite", "scikit-learn", "NumPy", "Pandas"],
    "DocumentAnalyser": ["FastAPI", "SQLite", "scikit-learn", "NumPy"],
    "CNN": ["React", "Vite", "Express", "MongoDB", "FastAPI", "PyTorch", "Docker"],
    "LEXA": ["Whisper", "PySide6", "SQLite", "NumPy", "pytest"],
    "AegisVault": ["FastAPI", "Pydantic", "SQLAlchemy", "PostgreSQL", "cryptography", "pytest"],
    "veildb": ["SQLAlchemy", "PostgreSQL", "cryptography", "pytest"],
    "URLShortener": ["FastAPI", "Pydantic", "SQLAlchemy", "PostgreSQL", "SQLite", "Redis", "pytest"],
    "Concord": ["React", "Vite", "Playwright"],
    "DevOS-AI-Software-Engineering-Agent": ["FastAPI", "Pydantic", "SQLite", "MCP"],
}


def point(radius, angle):
    radians = math.radians(angle)
    return round(900 + radius * math.cos(radians), 2), round(1060 + radius * math.sin(radians), 2)


def curve(source, target):
    sx, sy, tx, ty = source["x"], source["y"], target["x"], target["y"]
    # Bundle curves towards the centre; visible nodes are painted above edges.
    return f'M{sx} {sy}C{900+(sx-900)*.36:.2f} {1060+(sy-1060)*.36:.2f} {900+(tx-900)*.58:.2f} {1060+(ty-1060)*.58:.2f} {tx} {ty}'


def model(snapshot):
    user = snapshot["user"]
    repos = [r for r in snapshot["repositories"] if not r["fork"] and r["name"] != user]
    repos.sort(key=lambda r: r["name"].casefold())
    area_lookup = {name: area for area, names in AREAS.items() for name in names}
    groups = [{"id": key, "label": label, "color": color} for key, label, color in GROUPS]
    nodes = [{"id": "owner", "kind": "owner", "label": "ARPIT", "name": user,
              "x": 900, "y": 1060, "color": "#86f7cf", "url": f"https://github.com/{user}"}]
    edges = []
    start = -90
    nonempty = [g for g in groups if any(area_lookup.get(r["name"], "other") == g["id"] for r in repos)]
    available = 360-len(nonempty)*7
    for group in nonempty:
        members = [r for r in repos if area_lookup.get(r["name"], "other") == group["id"]]
        span = available * len(members)/len(repos)
        group.update(start=start, end=start+span, count=len(members))
        for i, repo in enumerate(members):
            angle = start + (i+.5)*span/len(members)
            x, y = point(610, angle)
            label = ALIASES.get(repo["name"], repo["name"])
            if len(label) > 26:
                label = label[:25]+"…"
            nodes.append({"id": "repo:"+repo["name"], "kind": "repository", "name": repo["name"],
                          "label": label, "x": x, "y": y, "angle": angle,
                          "group": group["id"], "area": group["label"], "color": group["color"],
                          "language": repo["language"], "url": f'https://github.com/{user}/{repo["name"]}'})
        start += span+7
    repo_nodes = [n for n in nodes if n["kind"] == "repository"]
    languages = sorted({r["language"] or "No language detected" for r in repos})
    for i, language in enumerate(languages):
        x, y = point(215, -90+i*360/len(languages))
        node = {"id": "language:"+language, "kind": "language", "label": language,
                "name": language, "x": x, "y": y, "color": "#86f7cf"}
        nodes.append(node)
        edges.append({"source": "owner", "target": node["id"], "kind": "portfolio", "color": "#86f7cf"})
        for repo in repo_nodes:
            if (repo["language"] or "No language detected") == language:
                edges.append({"source": node["id"], "target": repo["id"], "kind": "language",
                              "color": repo["color"], "evidence": "GitHub-detected primary language",
                              "url": repo["url"]})
    tool_names = sorted({tool for repo in repo_nodes for tool in TOOLS.get(repo["name"], [])})
    for i, tool in enumerate(tool_names):
        x, y = point(400, -90+(i+.3)*360/len(tool_names))
        node = {"id": "tool:"+tool, "kind": "tool", "label": tool, "name": tool,
                "x": x, "y": y, "color": "#b5a0ff"}
        nodes.append(node)
        for repo in repo_nodes:
            if tool in TOOLS.get(repo["name"], []):
                optional = repo["name"] == "URLShortener" and tool == "Redis"
                edges.append({"source": node["id"], "target": repo["id"], "kind": "tool", "color": "#b5a0ff",
                              "evidence": "Optional integration documented in README" if optional else "Tool documented in repository manifest or README",
                              "url": repo["url"]+"#readme", "optional": optional})
    lookup = {node["id"]: node for node in nodes}
    for i, edge in enumerate(edges):
        edge["id"] = f"edge-{i}"
        edge["path"] = curve(lookup[edge["source"]], lookup[edge["target"]])
    return {"user": user, "updated": snapshot["updated"], "width": 1800, "height": 2080,
            "nodes": nodes, "edges": edges, "groups": nonempty,
            "summary": {"repositories": len(repos), "languages": sum(lang != "No language detected" for lang in languages),
                        "tools": len(tool_names), "nodes": len(nodes), "connections": len(edges),
                        "forksExcluded": sum(r["fork"] for r in snapshot["repositories"])},
            "methodology": "Public non-fork repositories only. Areas are curated. Language links use GitHub metadata; tool links use reviewed project documentation. Connections do not imply dependencies between repositories. Motion is decorative."}


def artwork(data):
    counts = data["summary"]
    content = [
        '<rect x="2" y="2" width="1796" height="2076" rx="18" fill="url(#grid)"/>',
        '<text x="48" y="52" font-size="13" letter-spacing="3" class="mono mint">GITHUB WORK ATLAS / REPOSITORIES × LANGUAGES × TOOLS</text>',
        '<text x="45" y="112" font-size="48" font-weight="800" letter-spacing="-1">One portfolio. Many connected ideas.</text>',
        '<text x="48" y="150" font-size="18" class="muted">Explore the public projects, their primary languages, and documented technologies.</text>',
    ]
    for i, (value, label) in enumerate([(counts["repositories"], "REPOSITORIES"), (counts["languages"], "LANGUAGES"),
                                       (counts["tools"], "DOCUMENTED TOOLS"), (counts["connections"], "CONNECTIONS")]):
        x = 48+i*430
        content.append(f'<text x="{x}" y="211" font-size="27" font-weight="750" class="mint">{value}<tspan dx="14" font-size="12" letter-spacing="1.5" class="mono muted">{label}</tspan></text>')
    content.append('<path d="M48 240H1752" stroke="#253a35"/>')
    for radius in [215, 400, 570, 610]:
        content.append(f'<circle cx="900" cy="1060" r="{radius}" fill="none" stroke="#86f7cf" stroke-opacity=".09" stroke-dasharray="3 11"/>')
    for edge in data["edges"]:
        opacity = ".24" if edge["kind"] == "tool" else ".35"
        content.append(f'<path data-edge="{edge["id"]}" d="{edge["path"]}" stroke="{edge["color"]}" stroke-opacity="{opacity}" stroke-width="1.3" fill="none"/>')
    moving = [e for e in data["edges"] if e["kind"] != "portfolio"][::5]
    for i, edge in enumerate(moving):
        content.append(f'<circle r="3.5" fill="{edge["color"]}" opacity=".9" class="motion"><animateMotion path="{edge["path"]}" dur="{8+i%7}s" begin="-{i%11}s" repeatCount="indefinite"/></circle>')
    for group in data["groups"]:
        x1, y1 = point(570, group["start"])
        x2, y2 = point(570, group["end"])
        large = int(group["end"]-group["start"] > 180)
        mid = (group["start"]+group["end"])/2
        lx, ly = point(535, mid)
        content.append(f'<path d="M{x1} {y1}A570 570 0 {large} 1 {x2} {y2}" fill="none" stroke="{group["color"]}" stroke-width="3" opacity=".65"/>')
        content.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="12" class="mono" style="fill:{group["color"]}">{escape(group["label"])} · {group["count"]}</text>')
    for node in data["nodes"]:
        x, y, color = node["x"], node["y"], node["color"]
        content.append(f'<g data-node="{escape(node["id"], quote=True)}"><title>{escape(node["name"])} ({node["kind"]})</title>')
        if node["kind"] == "owner":
            content.append(f'<circle cx="{x}" cy="{y}" r="98" fill="#080c12" stroke="#86f7cf" stroke-opacity=".7"/><circle cx="{x}" cy="{y}" r="112" fill="none" stroke="#86f7cf" stroke-dasharray="15 12" opacity=".35" class="motion"><animateTransform attributeName="transform" type="rotate" from="0 {x} {y}" to="360 {x} {y}" dur="60s" repeatCount="indefinite"/></circle>')
            content.append(f'<text x="{x}" y="{y-12}" text-anchor="middle" font-size="30" font-weight="800">ARPIT</text><text x="{x}" y="{y+15}" text-anchor="middle" font-size="12" class="mono mint">PUBLIC WORK</text><text x="{x}" y="{y+41}" text-anchor="middle" font-size="11" class="muted">{counts["nodes"]} nodes</text>')
        elif node["kind"] == "repository":
            left = 90 < node["angle"] % 360 < 270
            rotation = node["angle"]+(180 if left else 0)
            dx, anchor = (-18, "end") if left else (18, "start")
            content.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{color}" stroke="#080c12" stroke-width="2"/><text transform="translate({x} {y}) rotate({rotation})" x="{dx}" y="5" text-anchor="{anchor}" font-size="18">{escape(node["label"])}</text>')
        else:
            label = node["label"]
            if label == "No language detected": label = "Not detected"
            width = max(76, len(label)*8+20)
            content.append(f'<rect x="{x-width/2}" y="{y-16}" width="{width}" height="32" rx="16" fill="#0c131d" stroke="{color}" stroke-opacity=".55"/><text x="{x}" y="{y+5}" text-anchor="middle" font-size="13" class="mono">{escape(label)}</text>')
        content.append('</g>')
    content.extend([
        '<path d="M48 1948H1752" stroke="#253a35"/>',
        '<text x="48" y="1988" font-size="14" class="mono mint">INNER / PRIMARY LANGUAGES</text>',
        '<text x="620" y="1988" font-size="14" class="mono violet">MIDDLE / DOCUMENTED TOOLS</text>',
        '<text x="1240" y="1988" font-size="14" class="mono muted">OUTER / REPOSITORIES BY AREA</text>',
        f'<text x="48" y="2026" font-size="14" class="muted">{counts["forksExcluded"]} forks excluded · snapshot {data["updated"]} UTC · areas curated · signals decorative</text>',
        '<text x="48" y="2052" font-size="13" class="muted">Connections show shared languages or documented tool use, not dependencies between repositories.</text>',
    ])
    return svg(1800, 2080, "Arpit's GitHub work atlas",
               f'{counts["repositories"]} repositories, {counts["languages"]} languages, {counts["tools"]} documented tools, and {counts["connections"]} connections. '+data["methodology"], "\n".join(content))


def build_atlas(snapshot):
    data = model(snapshot)
    graphic = artwork(data)
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # JSON is inert data, with HTML-significant characters escaped in the script element.
    encoded = encoded.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    template = Path(__file__).with_name("work_atlas.html").read_text()
    explorer = template.replace("__ATLAS_DATA__", encoded).replace("__ATLAS_SVG__", graphic)
    return {"work-atlas.svg": graphic,
            "work-atlas-data.json": json.dumps(data, indent=2, ensure_ascii=False)+"\n",
            "work-atlas.html": explorer}
