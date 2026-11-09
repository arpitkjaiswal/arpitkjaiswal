"""Self-contained, script-free SVG artwork for the GitHub profile."""

from html import escape
from itertools import combinations
import math


def svg(width, height, title, description, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
<linearGradient id="border"><stop stop-color="#174464"/><stop offset=".55" stop-color="#202b39"/><stop offset="1" stop-color="#3a3155"/></linearGradient>
<linearGradient id="accent"><stop stop-color="#78dcff"><animate attributeName="stop-color" values="#78dcff;#b5a0ff;#78dcff" dur="16s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="#b5a0ff"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#78dcff" stop-opacity=".18"/><stop offset="1" stop-color="#78dcff" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#78dcff" stroke-opacity=".045"/></pattern>
</defs>
<style>
text{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:#edf3f8}}
.muted{{fill:#99a8ba}}.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.mint{{fill:#78dcff}}.violet{{fill:#b5a0ff}}
.static-only{{display:none}}
@media(prefers-reduced-motion:reduce){{.motion{{display:none}}.static-only{{display:inline}}}}
</style>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="#070d18" stroke="url(#border)"/>
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


def wireframe_core(cx=1100, cy=240, radius=153):
    """Perspective-project a rotating icosahedron into script-free SVG frames."""
    phi = (1+math.sqrt(5))/2
    raw = [(0, a, b*phi) for a in (-1, 1) for b in (-1, 1)]
    raw += [(a, b*phi, 0) for a in (-1, 1) for b in (-1, 1)]
    raw += [(a*phi, 0, b) for a in (-1, 1) for b in (-1, 1)]
    scale = math.sqrt(1+phi*phi)
    vertices = [tuple(v/scale for v in point) for point in raw]
    distances = {(a, b): sum((vertices[a][i]-vertices[b][i])**2 for i in range(3))
                 for a, b in combinations(range(12), 2)}
    minimum = min(distances.values())
    edges = {pair for pair, distance in distances.items() if abs(distance-minimum) < 1e-6}
    faces = [face for face in combinations(range(12), 3)
             if all(tuple(sorted(pair)) in edges for pair in combinations(face, 2))]
    frames = []
    for frame in range(37):
        angle = frame/36*math.tau
        pitch = .4+.14*math.sin(angle)
        projected = []
        for x, y, z in vertices:
            x, z = x*math.cos(angle)+z*math.sin(angle), z*math.cos(angle)-x*math.sin(angle)
            y, z = y*math.cos(pitch)-z*math.sin(pitch), z*math.cos(pitch)+y*math.sin(pitch)
            perspective = 4/(4-z)
            projected.append((cx+x*radius*perspective, cy+y*radius*perspective, z))
        frames.append(projected)

    def path(frame, indices, close=False):
        return "M"+"L".join(f"{frame[i][0]:.2f} {frame[i][1]:.2f}" for i in indices)+("Z" if close else "")

    animated, static = [], []
    for face in faces:
        values = ";".join(path(frame, face, True) for frame in frames)
        base = f'<path d="{path(frames[0], face, True)}" fill="#78dcff" fill-opacity=".055"'
        animated.append(base+f'><animate attributeName="d" values="{values}" dur="28s" repeatCount="indefinite"/></path>')
        static.append(base+'/>')
    for edge in sorted(edges):
        values = ";".join(path(frame, edge) for frame in frames)
        opacity = ";".join(f"{.23+.4*(1+sum(frame[i][2] for i in edge)/2)/2:.3f}" for frame in frames)
        base = f'<path data-mesh-edge="true" d="{path(frames[0], edge)}" fill="none" stroke="#78dcff" stroke-width="1.65" stroke-opacity=".65"'
        animated.append(base+f'><animate attributeName="d" values="{values}" dur="28s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="{opacity}" dur="28s" repeatCount="indefinite"/></path>')
        static.append(base+'/>')
    for i in range(12):
        x, y, _ = frames[0][i]
        base = f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="#eefbff"'
        animation = "".join(f'<animate attributeName="{attr}" values="'+";".join(f"{frame[i][index]:.2f}" for frame in frames)+'" dur="28s" repeatCount="indefinite"/>' for attr, index in [("cx", 0), ("cy", 1)])
        animated.append(base+'>'+animation+'</circle>')
        static.append(base+'/>')
    return '<g class="motion">'+"".join(animated)+'</g><g class="static-only">'+"".join(static)+'</g>'


def header():
    ticks = []
    for i in range(60):
        angle = math.tau*i/60
        inner = 192 if i % 5 == 0 else 198
        x1, y1 = 1100+inner*math.cos(angle), 240+inner*math.sin(angle)
        x2, y2 = 1100+204*math.cos(angle), 240+204*math.sin(angle)
        ticks.append(f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" stroke="#86f7cf" stroke-opacity="{.45 if i%5==0 else .16}"/>')
    return svg(1400, 520, "Arpit Kumar Jaiswal — software developer",
               "Software engineering portfolio. Backend systems, developer tools, and applied AI. A decorative mathematical wireframe rotates in perspective; a static version is shown for reduced motion.", f'''
<rect x="2" y="2" width="1396" height="516" rx="18" fill="url(#grid)"/>
<circle cx="1100" cy="240" r="270" fill="url(#halo)"/>
<path d="M32 72V32H72M1328 32H1368V72M32 448V488H72M1328 488H1368V448" stroke="#86f7cf" stroke-opacity=".5" fill="none"/>
<text x="66" y="68" font-size="12" letter-spacing="3" class="mono mint">SOFTWARE ENGINEERING / ARPIT KUMAR JAISWAL</text>
<text x="60" y="176" font-size="94" font-weight="850" letter-spacing="-4">ARPIT KUMAR</text>
<text x="60" y="271" font-size="104" font-weight="850" letter-spacing="-4" class="mint">JAISWAL<tspan fill="#edf3f8">.</tspan></text>
<text x="67" y="321" font-size="23">From a problem to a working system.</text>
<text x="67" y="355" font-size="16" class="muted">Backend development / Developer tools / Applied AI</text>
<path d="M68 386H820" stroke="#233c35"/>
<text x="68" y="414" font-size="13" class="mono muted">B.Tech · Information Technology · MIT Manipal</text>
{''.join(ticks)}
<circle cx="1100" cy="240" r="211" fill="none" stroke="#86f7cf" stroke-opacity=".2"/>
<circle cx="1100" cy="240" r="220" fill="none" stroke="#b5a0ff" stroke-opacity=".55" stroke-dasharray="130 900" class="motion"><animateTransform attributeName="transform" type="rotate" from="0 1100 240" to="360 1100 240" dur="36s" repeatCount="indefinite"/></circle>
{wireframe_core()}
<text x="1100" y="480" text-anchor="middle" font-size="11" letter-spacing="3" class="mono mint">DESIGN / BUILD / VERIFY</text>
<circle cx="73" cy="470" r="4" fill="#86f7cf"/>
<text x="91" y="475" font-size="12" letter-spacing="1.5" class="mono mint">OPEN TO SOFTWARE ENGINEERING OPPORTUNITIES</text>
''')


def divider():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="48" viewBox="0 0 1200 48" role="img" aria-label="Animated mint signal divider">
<style>@media(prefers-reduced-motion:reduce){.motion{display:none}}</style>
<path d="M0 24H1200" stroke="#20312f"/><path d="M0 24H96M1104 24H1200" stroke="#86f7cf"/>
<path d="M0 24H80" stroke="#b5a0ff" stroke-width="2" class="motion"><animateTransform attributeName="transform" type="translate" values="0 0;1120 0;0 0" dur="18s" repeatCount="indefinite"/></path>
<path d="M592 24L600 16L608 24L600 32Z" fill="#080c12" stroke="#86f7cf"/>
</svg>\n'''


def architecture():
    columns = [
        ("NEXORA", "DEVELOPER TOOLING", "#86f7cf", [
            ("REACT / TYPESCRIPT", "Explore findings and dependency maps"),
            ("NODE.JS ANALYSIS API", "Imports, AST metrics, code checks"),
            ("GRAPH + ADVISORY SIGNALS", "Relative imports and npm advisories"),
            ("SAVED SNAPSHOTS", "Historical findings and review exports")]),
        ("TalentOS", "EXPLAINABLE RANKING", "#b5a0ff", [
            ("REACT / TYPESCRIPT", "Roles, candidates, and Resume Lab"),
            ("FASTAPI BOUNDARY", "Validated inputs and bounded extraction"),
            ("SCIKIT-LEARN", "Pairwise TF-IDF and skill coverage"),
            ("SQLALCHEMY / POSTGRESQL", "Transactional records and migrations")]),
        ("AegisVault", "ENCRYPTION RESEARCH", "#e8bc85", [
            ("PYTHON SDK / HTTP API", "Explicit document operations"),
            ("POLICY + MANIFEST", "Tenant, role, purpose, and contracts"),
            ("ENCRYPTION + SEARCH", "AEAD payloads and scoped HMAC terms"),
            ("DATABASE + AUDIT", "Atomic updates and authenticated events")]),
    ]
    content = ['<rect x="2" y="2" width="1396" height="756" rx="18" fill="url(#grid)"/>',
               '<text x="42" y="48" font-size="12" letter-spacing="2.5" class="mono mint">ENGINEERING BLUEPRINT / THREE IMPLEMENTATIONS</text>',
               '<text x="40" y="96" font-size="34" font-weight="750">From interface to system behavior.</text>']
    for i, (title, category, color, steps) in enumerate(columns):
        x = 42+i*448
        content.append(f'<text x="{x}" y="157" font-size="27" font-weight="750">{title}</text><text x="{x}" y="182" font-size="10" letter-spacing="1.5" class="mono" style="fill:{color}">{category}</text>')
        for j, (label, description) in enumerate(steps):
            y = 217+j*111
            if j:
                path = f"M{x+202} {y-28}V{y}"
                content.append(f'<path d="{path}" stroke="{color}" stroke-opacity=".5"/><path d="M{x+198} {y-7}L{x+202} {y-2}L{x+206} {y-7}" fill="none" stroke="{color}"/>')
                content.append(f'<circle r="2.8" fill="{color}" class="motion"><animateMotion path="{path}" dur="2s" begin="-{j*.6}s" repeatCount="indefinite"/></circle>')
            content.append(f'<rect x="{x}" y="{y}" width="404" height="83" rx="10" fill="#0d141c" stroke="{color}" stroke-opacity=".25"/><path d="M{x} {y+15}V{y+68}" stroke="{color}" stroke-width="2"/>')
            content.append(f'<text x="{x+19}" y="{y+31}" font-size="12" letter-spacing=".8" class="mono" style="fill:{color}">{label}</text><text x="{x+19}" y="{y+58}" font-size="13" class="muted">{description}</text>')
    content.append('<path d="M42 685H1358" stroke="#26383a"/><text x="42" y="716" font-size="12" class="muted">Conceptual request paths from project documentation. Each application has its own scope and deployment model.</text>')
    return svg(1400, 760, "Architecture of NEXORA, TalentOS, and AegisVault",
               "Three documented application paths: repository analysis, explainable candidate ranking, and policy-aware encrypted document storage. Moving signals illustrate the paths and do not represent live traffic.", "\n".join(content))


def project_card(key):
    projects = {
        "nexora": ("01", "DEVELOPER TOOLS", "NEXORA", "Read the codebase.", "Find what matters.",
                   "REACT / TYPESCRIPT / NODE.JS", "#78dcff"),
        "talentos": ("02", "EXPLAINABLE ML", "TalentOS", "Rank with evidence.", "Keep the reasoning visible.",
                     "FASTAPI / REACT / SCIKIT-LEARN", "#b5a0ff"),
        "aegisvault": ("03", "SECURITY RESEARCH", "AegisVault", "Make data boundaries explicit.", "Policy. Encryption. Audit.",
                       "PYTHON / POSTGRESQL / CRYPTOGRAPHY", "#e8bc85"),
    }
    index, category, title, tagline, second_line, tools, color = projects[key]
    art = []
    if key == "nexora":
        points = [(66, 224), (182, 192), (182, 255), (344, 224)]
        for a, b in [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]:
            x1, y1 = points[a]; x2, y2 = points[b]
            path = f"M{x1} {y1}L{x2} {y2}"
            art.append(f'<path d="{path}" stroke="{color}" stroke-opacity=".4"/>')
            art.append(f'<circle r="2.5" fill="{color}" class="motion"><animateMotion path="{path}" dur="4.7s" begin="-{a}s" repeatCount="indefinite"/></circle>')
        for i, (x, y) in enumerate(points):
            art.append(f'<rect x="{x-25}" y="{y-18}" width="50" height="36" rx="8" fill="#0b1928" stroke="{color}" stroke-opacity=".65"/><text x="{x}" y="{y+4}" text-anchor="middle" font-size="10" class="mono">{["SRC","API","MAP","REVIEW"][i]}</text>')
    elif key == "talentos":
        for i, label in enumerate(["RESUME", "MODEL", "EVIDENCE"]):
            x = 27+i*135
            art.append(f'<rect x="{x}" y="191" width="113" height="70" rx="9" fill="#141329" stroke="{color}" stroke-opacity=".35"/><text x="{x+56}" y="219" text-anchor="middle" font-size="10" class="mono violet">{label}</text><path d="M{x+22} 234H{x+91}M{x+22} 245H{x+75}" stroke="{color}" stroke-opacity=".35"/>')
            if i<2:
                path=f'M{x+113} 226H{x+135}'
                art.append(f'<path d="{path}" stroke="{color}" stroke-opacity=".5"/><circle r="2.4" fill="{color}" class="motion"><animateMotion path="{path}" dur="2.7s" begin="-{i}s" repeatCount="indefinite"/></circle>')
    else:
        art.append(f'<path d="M222 175L262 192V223Q262 253 222 275Q182 253 182 223V192Z" fill="#211d17" stroke="{color}" stroke-width="1.5"/>')
        art.append(f'<rect x="208" y="216" width="28" height="25" rx="4" fill="none" stroke="{color}" stroke-width="1.6"/><path d="M213 216V208A9 9 0 0 1 231 208V216" fill="none" stroke="{color}" stroke-width="1.6"/>')
        for x, label in [(70,"POLICY"),(375,"AUDIT")]:
            art.append(f'<circle cx="{x}" cy="226" r="23" fill="#171923" stroke="{color}" stroke-opacity=".4"/><text x="{x}" y="270" text-anchor="middle" font-size="10" class="mono" style="fill:{color}">{label}</text>')
        for path in ['M93 226H181','M263 226H352']:
            art.append(f'<path d="{path}" stroke="{color}" stroke-opacity=".4"/><circle r="2.5" fill="{color}" class="motion"><animateMotion path="{path}" dur="3.7s" repeatCount="indefinite"/></circle>')
    content = f'''
<rect x="2" y="2" width="446" height="346" rx="18" fill="url(#grid)"/>
<path d="M20 45V20H45M403 330H428V305" stroke="{color}" stroke-opacity=".5" fill="none"/>
<text x="27" y="43" font-size="11" letter-spacing="1.2" class="mono" style="fill:{color}">{index} / {category}</text>
<text x="24" y="101" font-size="47" font-weight="800" letter-spacing="-1.5">{title}</text>
<text x="27" y="132" font-size="15">{tagline}</text>
<text x="27" y="155" font-size="14" class="muted">{second_line}</text>
<path d="M27 292H421" stroke="{color}" stroke-opacity=".2"/>
<text x="27" y="321" font-size="10.5" class="mono" style="fill:{color}">{tools}</text>
{''.join(art)}
'''
    return svg(450, 350, f"{title} — {category.lower()}", tagline+" "+second_line+" Decorative project illustration.", content)


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
        '<text x="32" y="77" font-size="16" class="muted">Tools used in the repositories linked here.</text>',
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
