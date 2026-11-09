"""Generate local brand-icon tiles and contact buttons from vendored SVGs."""

from functools import lru_cache
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [
    ("Languages & foundations", ["python", "typescript", "javascript", "java", "c", "cplusplus", "html5", "css3"]),
    ("Web & APIs", ["react", "vite", "nodedotjs", "express", "fastapi", "pydantic"]),
    ("Databases & storage", ["postgresql", "mongodb", "redis", "sqlite", "sqlalchemy"]),
    ("Machine learning & data", ["pytorch", "scikitlearn", "numpy", "pandas", "scipy"]),
    ("Tools & delivery", ["docker", "git", "github", "githubactions", "linux", "pytest", "playwright", "ruff", "uv"]),
    ("AI integrations", ["openai", "anthropic", "ollama"]),
]
DOCS = {
    "python": "https://www.python.org/", "typescript": "https://www.typescriptlang.org/",
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "java": "https://dev.java/",
    "c": "https://en.cppreference.com/w/c", "cplusplus": "https://isocpp.org/",
    "html5": "https://developer.mozilla.org/en-US/docs/Web/HTML", "css3": "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "react": "https://react.dev/", "vite": "https://vite.dev/", "nodedotjs": "https://nodejs.org/",
    "express": "https://expressjs.com/", "fastapi": "https://fastapi.tiangolo.com/", "pydantic": "https://docs.pydantic.dev/",
    "postgresql": "https://www.postgresql.org/", "mongodb": "https://www.mongodb.com/", "redis": "https://redis.io/",
    "sqlite": "https://www.sqlite.org/", "sqlalchemy": "https://www.sqlalchemy.org/", "pytorch": "https://pytorch.org/",
    "scikitlearn": "https://scikit-learn.org/", "numpy": "https://numpy.org/", "pandas": "https://pandas.pydata.org/",
    "scipy": "https://scipy.org/", "docker": "https://www.docker.com/", "git": "https://git-scm.com/",
    "github": "https://github.com/", "githubactions": "https://github.com/features/actions", "linux": "https://www.kernel.org/",
    "pytest": "https://docs.pytest.org/", "playwright": "https://playwright.dev/", "ruff": "https://docs.astral.sh/ruff/",
    "uv": "https://docs.astral.sh/uv/", "openai": "https://platform.openai.com/docs/",
    "anthropic": "https://docs.anthropic.com/", "ollama": "https://ollama.com/",
}
CONTACTS = {
    "linkedin": ("linkedin", "LinkedIn", "Let’s connect", "#3695f0", "https://www.linkedin.com/in/arpit-kumar-jaiswal-819478302"),
    "email": ("gmail", "Email", "Say hello", "#f27169", "mailto:arpit.kr.jaiswal@gmail.com"),
    "github": ("github", "GitHub", "Explore the code", "#dceaff", "https://github.com/arpitkjaiswal?tab=repositories"),
}
# Preserve recognizable shapes and keep very dark brand marks visible on navy.
DARK_MODE_COLORS = {"github": "#edf3f8", "express": "#edf3f8", "anthropic": "#e8c7b0",
                    "ollama": "#edf3f8", "numpy": "#6bbbd1", "pandas": "#bea7ff",
                    "sqlite": "#78c5e8", "openai": "#b4a2f4", "cplusplus": "#5caaf2"}


@lru_cache(maxsize=1)
def catalog():
    return json.loads((ROOT / "assets/icon-sources.json").read_text())["icons"]


def logo(slug, x, y, size, color=None):
    record = catalog()[slug]
    source = record["svg"]
    parsed = ET.fromstring(source)
    viewbox = parsed.attrib.get("viewBox", "0 0 24 24")
    inner = re.search(r"<svg\b[^>]*>(.*)</svg\s*>", source, re.S).group(1)
    inner = re.sub(r"<(title|desc)\b[^>]*>.*?</\1>", "", inner, flags=re.S)
    foreground = color or DARK_MODE_COLORS.get(slug, "#"+record["hex"])
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{viewbox}" '
            f'fill="{foreground}" aria-hidden="true">{inner}</svg>')


def tile(slug):
    record = catalog()[slug]
    name = record["title"]
    color = DARK_MODE_COLORS.get(slug, "#"+record["hex"])
    font = 8.2 if len(name)>11 else 9.2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="80" height="90" viewBox="0 0 80 90" role="img" aria-label="{escape(name, quote=True)}">
<title>{escape(name)}</title>
<defs><linearGradient id="tile" x2="1" y2="1"><stop stop-color="#102139"/><stop offset="1" stop-color="#080e1b"/></linearGradient></defs>
<rect x="1" y="1" width="78" height="88" rx="12" fill="url(#tile)" stroke="#263b56"/>
<path d="M15 1H65" stroke="{color}" stroke-opacity=".65"/>
{logo(slug, 20, 14, 40)}
<text x="40" y="76" text-anchor="middle" fill="#edf3f8" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="{font}">{escape(name)}</text>
</svg>
'''


def contact_button(key):
    slug, title, caption, color, _ = CONTACTS[key]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="220" height="68" viewBox="0 0 220 68" role="img" aria-label="{escape(title+': '+caption, quote=True)}">
<title>{escape(title)} — {escape(caption)}</title>
<style>@media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}</style>
<defs><linearGradient id="panel"><stop stop-color="#102039"/><stop offset="1" stop-color="#080f1d"/></linearGradient></defs>
<rect x="1" y="1" width="218" height="66" rx="12" fill="url(#panel)" stroke="#2a4260"/>
{logo(slug, 17, 18, 32, color)}
<text x="64" y="30" fill="#edf3f8" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-weight="700" font-size="18">{escape(title)}</text>
<text x="64" y="49" fill="#a5b7ca" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="11">{escape(caption)}</text>
<path d="M192 27L199 34L192 41M185 34H199" fill="none" stroke="{color}" stroke-width="1.5"/>
<path d="M16 66H204" stroke="{color}" stroke-opacity=".22"/>
<path d="M16 66H49" stroke="{color}" stroke-opacity=".8" class="motion"><animateTransform attributeName="transform" type="translate" values="0 0;155 0;0 0" dur="9s" repeatCount="indefinite"/></path>
</svg>
'''


def build_icon_artwork():
    files = {f"icons/{slug}.svg": tile(slug) for _, slugs in GROUPS for slug in slugs}
    files.update({f"contact/{key}.svg": contact_button(key) for key in CONTACTS})
    return files
