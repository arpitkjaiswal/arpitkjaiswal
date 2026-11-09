"""Self-contained, script-free SVG artwork for the GitHub profile."""

from html import escape


def svg(width, height, title, description, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
<linearGradient id="border"><stop stop-color="#28433f"/><stop offset=".55" stop-color="#202b39"/><stop offset="1" stop-color="#3a3155"/></linearGradient>
<linearGradient id="accent"><stop stop-color="#86f7cf"><animate attributeName="stop-color" values="#86f7cf;#b5a0ff;#86f7cf" dur="16s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="#b5a0ff"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#86f7cf" stop-opacity=".13"/><stop offset="1" stop-color="#86f7cf" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#86f7cf" stroke-opacity=".045"/></pattern>
</defs>
<style>
text{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:#edf3f8}}
.muted{{fill:#99a8ba}}.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.mint{{fill:#86f7cf}}.violet{{fill:#b5a0ff}}
@media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}
</style>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="#080c12" stroke="url(#border)"/>
{content}
</svg>
'''


def orbit(cx, cy, radius, color="#86f7cf"):
    """A static core remains visible when decorative motion is reduced."""
    return f'''<circle cx="{cx}" cy="{cy}" r="{radius}" fill="url(#halo)"/>
<ellipse cx="{cx}" cy="{cy}" rx="{radius}" ry="{radius*.36}" fill="none" stroke="{color}" stroke-opacity=".35" transform="rotate(-32 {cx} {cy})"/>
<ellipse cx="{cx}" cy="{cy}" rx="{radius}" ry="{radius*.36}" fill="none" stroke="{color}" stroke-opacity=".35" transform="rotate(32 {cx} {cy})"/>
<g class="motion"><circle cx="{cx}" cy="{cy}" r="{radius*.82}" fill="none" stroke="{color}" stroke-width="1.5" stroke-dasharray="80 18 2 18" opacity=".65"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="35s" repeatCount="indefinite"/></circle>
<circle cx="{cx}" cy="{cy}" r="{radius*.62}" fill="none" stroke="#b5a0ff" stroke-dasharray="3 14" opacity=".8"><animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="24s" repeatCount="indefinite"/></circle></g>'''


def header():
    grid = []
    for x in range(-300, 1600, 100):
        grid.append(f'<path d="M940 330L{x} 520" stroke="#86f7cf" opacity=".09"/>')
    for y in [350, 368, 394, 430, 480]:
        grid.append(f'<path d="M600 {y}H1200" stroke="#86f7cf" opacity=".06"/>')
    stars = "".join(
        f'<circle cx="{(i*137+41)%1160+20}" cy="{(i*67+23)%370+20}" r="1" fill="#86f7cf" opacity=".3"/>'
        for i in range(28)
    )
    core = []
    # An isometric wireframe cube, with a moving signal around its perimeter.
    for path in ["M944 155L1006 191V263L944 299L882 263V191Z",
                 "M882 191L944 227L1006 191M944 227V299",
                 "M944 155V227M882 263L944 227L1006 263"]:
        core.append(f'<path d="{path}" fill="none" stroke="#86f7cf" stroke-opacity=".65" stroke-width="1.5"/>')
    core.append('''<circle r="3" fill="#fff" class="motion"><animateMotion path="M944 155L1006 191V263L944 299L882 263V191Z" dur="10s" repeatCount="indefinite"/></circle>''')
    return svg(1200, 520, "Arpit Kumar Jaiswal — backend, full-stack, and applied AI",
               "Animated engineering console with an orbital wireframe core. Open to software engineering opportunities.", f'''
<rect x="2" y="2" width="1196" height="516" rx="18" fill="url(#grid)"/>
{stars}
<circle cx="946" cy="220" r="265" fill="url(#halo)"/>
<path d="M32 72V32H72M1128 32H1168V72M32 448V488H72M1128 488H1168V448" fill="none" stroke="#86f7cf" stroke-opacity=".45"/>
<text x="64" y="62" font-size="12" letter-spacing="2.5" class="mono mint">ARPIT / SOFTWARE DEVELOPER</text>
<text x="1136" y="62" font-size="11" text-anchor="end" letter-spacing="2" class="mono muted">BUILD. UNDERSTAND. ITERATE.</text>
<text x="60" y="173" font-size="84" font-weight="850" letter-spacing="-4">ARPIT KUMAR</text>
<text x="60" y="263" font-size="92" font-weight="850" letter-spacing="-4" class="mint">JAISWAL<tspan fill="#edf3f8">.</tspan></text>
<text x="66" y="311" font-size="20">Backend systems. Applied AI. Thoughtful interfaces.</text>
<text x="66" y="343" font-size="14" class="mono muted">B.Tech · Information Technology · MIT Manipal</text>
<circle cx="72" cy="387" r="4" fill="#86f7cf"/>
<text x="88" y="392" font-size="12" letter-spacing="1.2" class="mono mint">OPEN TO SOFTWARE ENGINEERING OPPORTUNITIES</text>
{''.join(grid)}
{orbit(944, 227, 163)}
{''.join(core)}
<text x="944" y="426" text-anchor="middle" font-size="10" letter-spacing="3" class="mono muted">IDEA → SYSTEM</text>
<rect x="52" y="446" width="1096" height="42" rx="8" fill="#0d151c" stroke="#20332f"/>
<circle cx="72" cy="467" r="3" fill="#86f7cf"/><circle cx="86" cy="467" r="3" fill="#b5a0ff"/><circle cx="100" cy="467" r="3" fill="#e8bc85"/>
<text x="128" y="472" font-size="13" class="mono"><tspan fill="#86f7cf">arpit@build</tspan><tspan fill="#99a8ba">:~$ </tspan>turn curiosity into working software<tspan class="motion"> ▍<animate attributeName="opacity" values="1;1;0;0;1" dur="2s" repeatCount="indefinite"/></tspan></text>
<text x="1124" y="472" text-anchor="end" font-size="11" class="mono muted">PY / TS</text>
''')


def divider():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="48" viewBox="0 0 1200 48" role="img" aria-label="Animated mint signal divider">
<style>@media(prefers-reduced-motion:reduce){.motion{display:none}}</style>
<path d="M0 24H1200" stroke="#20312f"/><path d="M0 24H96M1104 24H1200" stroke="#86f7cf"/>
<path d="M0 24H80" stroke="#b5a0ff" stroke-width="2" class="motion"><animateTransform attributeName="transform" type="translate" values="0 0;1120 0;0 0" dur="18s" repeatCount="indefinite"/></path>
<path d="M592 24L600 16L608 24L600 32Z" fill="#080c12" stroke="#86f7cf"/>
</svg>\n'''


def architecture():
    nodes = [
        (54, 95, "01", "INTERFACES", "React / TypeScript / Vite", "#86f7cf"),
        (54, 205, "02", "BACKEND", "FastAPI / Node.js / Express", "#86f7cf"),
        (54, 315, "03", "DATA", "PostgreSQL / Redis / SQLite", "#86f7cf"),
        (856, 95, "04", "APPLIED AI", "PyTorch / scikit-learn / MCP", "#b5a0ff"),
        (856, 205, "05", "SECURITY", "Encryption / policy / audit", "#b5a0ff"),
        (856, 315, "06", "DELIVERY", "Docker / pytest / Playwright", "#b5a0ff"),
    ]
    content = ['<rect x="2" y="2" width="1196" height="456" rx="18" fill="url(#grid)"/>',
               '<text x="32" y="43" font-size="12" letter-spacing="2" class="mono mint">SYSTEM VIEW / CONNECTING THE LAYERS</text>']
    for i, (x, y, index, label, tools, color) in enumerate(nodes):
        target_x = x+290 if x < 600 else x
        path = f"M600 253 C{target_x} 253 600 {y+40} {target_x} {y+40}"
        content.append(f'<path d="{path}" stroke="{color}" opacity=".25" fill="none"/>')
        content.append(f'<circle r="3" fill="{color}" class="motion"><animateMotion path="{path}" dur="{5+i%3}s" begin="-{i}s" repeatCount="indefinite"/></circle>')
        content.append(f'<rect x="{x}" y="{y}" width="290" height="84" rx="10" fill="#0d141e" stroke="#283544"/>')
        content.append(f'<text x="{x+18}" y="{y+28}" font-size="11" letter-spacing="2" class="mono" style="fill:{color}">{index} / {label}</text>')
        content.append(f'<text x="{x+18}" y="{y+58}" font-size="13">{tools}</text>')
    content.append(orbit(600, 253, 111))
    content.append('''<circle cx="600" cy="253" r="60" fill="#080c12" stroke="#86f7cf" stroke-opacity=".5"/>
<text x="600" y="248" text-anchor="middle" font-size="24" font-weight="800">BUILD</text>
<text x="600" y="271" text-anchor="middle" font-size="10" class="mono muted">END TO END</text>
<text x="600" y="435" text-anchor="middle" font-size="11" class="mono muted">Interfaces → APIs → data → useful outcomes</text>''')
    return svg(1200, 460, "Engineering across the stack",
               "Animated overview of the technologies connected across Arpit's projects.", "\n".join(content))


def project_card(key):
    projects = {
        "nexora": ("01", "DEVELOPER TOOLING", "NEXORA", "Understand a codebase. Find what matters.",
                   "REACT / TYPESCRIPT / NODE.JS", "#86f7cf"),
        "talentos": ("02", "APPLIED MACHINE LEARNING", "TalentOS", "Candidate ranking you can inspect and explain.",
                     "FASTAPI / REACT / SCIKIT-LEARN", "#b5a0ff"),
        "aegisvault": ("03", "SECURITY RESEARCH PROTOTYPE", "AegisVault", "Policy-aware reads. Verifiable audit trails.",
                       "PYTHON / POSTGRESQL / CRYPTOGRAPHY", "#e8bc85"),
    }
    index, category, title, tagline, stack, color = projects[key]
    art = []
    if key == "nexora":
        points = [(870, 62), (1040, 87), (945, 142), (837, 208), (1070, 218)]
        for a, b in [(0, 2), (1, 2), (2, 3), (2, 4), (0, 1), (3, 4)]:
            x1, y1 = points[a]; x2, y2 = points[b]
            path = f"M{x1} {y1}L{x2} {y2}"
            art.append(f'<path d="{path}" stroke="{color}" stroke-opacity=".3"/>')
            art.append(f'<circle r="2" fill="{color}" class="motion"><animateMotion path="{path}" dur="4s" begin="-{a}s" repeatCount="indefinite"/></circle>')
        for i, (x, y) in enumerate(points):
            art.append(f'<rect x="{x-17}" y="{y-17}" width="34" height="34" rx="8" fill="#0d211e" stroke="{color}" stroke-opacity=".65"/><text x="{x}" y="{y+4}" text-anchor="middle" font-size="11" class="mono mint">{["UI","API","MAP","DEP","REV"][i]}</text>')
    elif key == "talentos":
        # Equal, decorative tracks: these are not fabricated candidate scores.
        for i in range(3):
            y = 70+i*62
            art.append(f'<rect x="825" y="{y}" width="285" height="43" rx="9" fill="#131122" stroke="#39304e"/>')
            art.append(f'<circle cx="849" cy="{y+21}" r="9" fill="#b5a0ff" opacity=".6"/><path d="M874 {y+16}H1010M874 {y+27}H978" stroke="#b5a0ff" opacity=".4"/>')
            art.append(f'<circle cx="1084" cy="{y+21}" r="4" fill="#b5a0ff" class="motion"><animate attributeName="opacity" values=".25;1;.25" dur="4s" begin="-{i}s" repeatCount="indefinite"/></circle>')
        art.append('<path d="M812 48H1124V251H812Z" fill="none" stroke="#b5a0ff" stroke-opacity=".12"/>')
    else:
        art.append(orbit(964, 147, 105, color))
        art.append(f'<path d="M964 78L1017 101V146Q1017 183 964 211Q911 183 911 146V101Z" fill="#1e1913" stroke="{color}" stroke-width="1.5"/>')
        art.append(f'<rect x="945" y="138" width="38" height="32" rx="5" fill="none" stroke="{color}" stroke-width="2"/><path d="M952 138V128A12 12 0 0 1 976 128V138" fill="none" stroke="{color}" stroke-width="2"/>')
        art.append(f'<circle cx="964" cy="153" r="3" fill="{color}"/>')
    content = f'''
<rect x="2" y="2" width="1196" height="286" rx="18" fill="url(#grid)"/>
<path d="M28 42V28H64M1136 262H1172V226" stroke="{color}" stroke-opacity=".5" fill="none"/>
<text x="50" y="60" font-size="12" letter-spacing="2" class="mono" style="fill:{color}">{index} / {category}</text>
<text x="46" y="141" font-size="70" font-weight="800" letter-spacing="-2">{title}</text>
<text x="50" y="184" font-size="19" class="muted">{tagline}</text>
<text x="50" y="239" font-size="12" letter-spacing="1" class="mono" style="fill:{color}">{stack}</text>
<path d="M760 40V250" stroke="#243039"/>
{''.join(art)}
'''
    return svg(1200, 290, f"{title} — {category.lower()}", tagline+" Decorative project illustration.", content)


def stack():
    groups = [
        ("01", "LANGUAGES", "Python · TypeScript · JavaScript", "Java · C · C++ · SQL"),
        ("02", "WEB &amp; APIs", "React · Vite · Node.js · Express", "FastAPI · Pydantic · MCP"),
        ("03", "DATA &amp; STORAGE", "PostgreSQL · SQLAlchemy · Alembic", "MongoDB · Redis · SQLite"),
        ("04", "MACHINE LEARNING", "PyTorch · scikit-learn · Whisper", "NumPy · Pandas · SciPy"),
        ("05", "DELIVERY &amp; QUALITY", "Docker · GitHub Actions · Linux", "pytest · Playwright · Ruff · uv"),
        ("06", "AI INTEGRATIONS", "OpenAI · Anthropic · Ollama", "Provider adapters · local models"),
    ]
    content = [
        '<text x="32" y="43" font-size="12" letter-spacing="2" class="mono mint">TECHNOLOGY INDEX / TOOLS IN CONTEXT</text>',
        '<text x="32" y="77" font-size="16" class="muted">A toolkit shaped by the projects below the badges.</text>',
    ]
    for i, (index, title, row1, row2) in enumerate(groups):
        x, y = 32+(i%3)*389, 110+(i//3)*146
        content.append(f'<rect x="{x}" y="{y}" width="358" height="122" rx="10" fill="#0d141c" stroke="#243239"/>')
        content.append(f'<text x="{x+18}" y="{y+28}" font-size="11" letter-spacing="1.5" class="mono mint">{index} / {title}</text>')
        content.append(f'<text x="{x+18}" y="{y+62}" font-size="14">{row1}</text><text x="{x+18}" y="{y+87}" font-size="13" class="muted">{row2}</text>')
        content.append(f'<circle cx="{x+334}" cy="{y+25}" r="3" fill="#86f7cf" class="motion"><animate attributeName="opacity" values=".25;.8;.25" dur="5s" begin="-{i}s" repeatCount="indefinite"/></circle>')
    return svg(1200, 410, "Project technology index",
               "Languages, APIs, storage, machine learning, delivery, and optional AI integrations present in Arpit's projects.", "\n".join(content))


def footer():
    return svg(1200, 220, "Let's build something worth using",
               "Open to software engineering opportunities and collaborations. Contact links follow this artwork.", '''
<rect x="2" y="2" width="1196" height="216" rx="18" fill="url(#grid)"/>
<text x="48" y="52" font-size="12" letter-spacing="2" class="mono mint">NEXT / A CONVERSATION</text>
<text x="46" y="112" font-size="44" font-weight="750" letter-spacing="-1">Let’s build something worth using.</text>
<text x="48" y="151" font-size="17" class="muted">A challenging problem. A thoughtful team. A chance to contribute.</text>
<path d="M48 184H1152" stroke="#243b35"/>
<path d="M48 184H180" stroke="#86f7cf" stroke-width="2" class="motion"><animateTransform attributeName="transform" type="translate" values="0 0;970 0;0 0" dur="16s" repeatCount="indefinite"/></path>
''')
