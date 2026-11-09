<div align="center">

<img src="./assets/header.svg" width="100%" alt="Arpit Kumar Jaiswal — software developer. Animated 3D engineering portfolio. Backend systems, developer tools, and applied AI. B.Tech Information Technology, MIT Manipal." />

**[Selected work](#selected-work)** &nbsp; / &nbsp; **[Engineering](#engineering)** &nbsp; / &nbsp; **[Toolbox](#toolbox)** &nbsp; / &nbsp; **[GitHub atlas](#github-work-atlas)** &nbsp; / &nbsp; **[Contact](#contact)**

</div>

I’m **Arpit Kumar Jaiswal**, a developer from **MIT Manipal**. I build with **Python and TypeScript**, working across backend systems, developer tools, and applied AI. My projects focus on making complicated systems easier to understand, use, and verify.

<p align="left">
<a href="https://www.linkedin.com/in/arpit-kumar-jaiswal-819478302"><img src="./assets/contact/linkedin.svg" width="176" alt="LinkedIn: Let’s connect" /></a>
<a href="mailto:arpit.kr.jaiswal@gmail.com"><img src="./assets/contact/email.svg" width="176" alt="Email: Say hello" /></a>
<a href="https://github.com/arpitkjaiswal?tab=repositories"><img src="./assets/contact/github.svg" width="176" alt="GitHub: Explore the code" /></a>
</p>

[Read the engineering walkthroughs](./docs/engineering-notes.md)

## Selected work

<div align="center">

<a href="https://github.com/arpitkjaiswal/NEXORA"><img src="./assets/project-nexora.svg" width="32%" alt="NEXORA: repository analysis and developer tooling, built with React, TypeScript, and Node.js. Open the source repository." /></a>
<a href="https://github.com/arpitkjaiswal/Candidate-Ranking-System"><img src="./assets/project-talentos.svg" width="32%" alt="TalentOS: explainable candidate ranking with React, FastAPI, and scikit-learn. Open the source repository." /></a>
<a href="https://github.com/arpitkjaiswal/AegisVault"><img src="./assets/project-aegisvault.svg" width="32%" alt="AegisVault: policy-aware encryption research using Python and PostgreSQL. Open the source repository." /></a>

</div>

### NEXORA

**Make a codebase easier to navigate.** A repository analysis workspace connecting import graphs, AST-based metrics, code findings, npm advisories, and saved review snapshots.

**Engineering to inspect:** relative-import resolution, signed webhook delivery deduplication, and a rules-based review path with an optional AI adapter.

[Source](https://github.com/arpitkjaiswal/NEXORA) · [Design decisions](./docs/engineering-notes.md#nexora--turn-source-analysis-into-something-a-developer-can-use) · [Build & verification](https://github.com/arpitkjaiswal/NEXORA#validation)

### TalentOS

**Show the evidence behind a ranking.** A React/FastAPI candidate workspace with explainable lexical and skill scoring, excerpts, skill gaps, and a private Resume Lab.

**Engineering to inspect:** bounded extraction workers, independent resume/JD scoring, transactional uploads, and stale-write protection.

[Source](https://github.com/arpitkjaiswal/Candidate-Ranking-System) · [Design decisions](./docs/engineering-notes.md#talentos--make-a-ranking-explainable-and-reviewable) · [Recorded verification](https://github.com/arpitkjaiswal/Candidate-Ranking-System/blob/HEAD/docs/VALIDATION.md)

<details>
<summary><b>Product preview — recruiter workspace with synthetic demonstration data</b></summary>

<br />

<img src="./assets/talentos-workspace.png" width="100%" alt="TalentOS recruiter dashboard: role context, synthetic candidate shortlist, evidence, workflow stages, and workspace activity" />

Original screenshot from the [project documentation](https://github.com/arpitkjaiswal/Candidate-Ranking-System/blob/b3b70df9248662c7c166f1c36c49a75c78eae4c2/docs/overview.png). Example candidates and scores describe the demonstration workspace.

</details>

### AegisVault

**Make data boundaries explicit.** A Python SDK and HTTP API for policy-gated encrypted records, tenant-scoped exact search, and authenticated audit chains.

**Engineering to inspect:** manifest-bound interpretation, atomic record/search-term updates, optimistic revisions, and plaintext release after read-audit commit. Research prototype; not independently security-audited.

[Source](https://github.com/arpitkjaiswal/AegisVault) · [Design decisions](./docs/engineering-notes.md#aegisvault--make-the-data-boundary-explicit) · [Security boundaries](https://github.com/arpitkjaiswal/AegisVault/blob/HEAD/docs/security.md) · [Recorded verification](https://github.com/arpitkjaiswal/AegisVault/blob/HEAD/docs/status.md)

<details>
<summary><b>More work: voice interfaces, computer vision, document search, and developer tools</b></summary>

<br />

| Project | What to explore | Stack |
| :--- | :--- | :--- |
| [**LEXA**](https://github.com/arpitkjaiswal/LEXA) | macOS-first AI desktop companion with voice recognition and allowlisted local skills | Python · Whisper · PySide6 |
| [**LeafScan**](https://github.com/arpitkjaiswal/CNN) | Leaf-photo classification, account flows, and private scan history | React · Express · MongoDB · PyTorch |
| [**DevOS**](https://github.com/arpitkjaiswal/DevOS-AI-Software-Engineering-Agent) | Read-only repository investigations with durable run state and human review | FastAPI · SQLite · MCP |
| [**DocumentAnalyser**](https://github.com/arpitkjaiswal/DocumentAnalyser) | PDF/DOCX extraction, document retrieval, and optional provider-backed answers | FastAPI · scikit-learn · SQLite |
| [**URLShortener**](https://github.com/arpitkjaiswal/URLShortener) | Link management, aliases, expiry, QR downloads, and private analytics | FastAPI · SQLAlchemy · PostgreSQL |
| [**veildb**](https://github.com/arpitkjaiswal/veildb) | Searchable-encryption research for PostgreSQL applications | Python · cryptography · SQLAlchemy |
| [**Concord**](https://github.com/arpitkjaiswal/Concord) | A workspace for organizing ideas and getting work done | React · TypeScript · Vite |
| [**CommitSync**](https://github.com/arpitkjaiswal/CommitSync) | Chrome extension for syncing accepted LeetCode solutions to GitHub | JavaScript · Browser APIs |

</details>

<img src="./assets/divider.svg" width="100%" alt="Animated signal divider" />

## Engineering

I care about the behavior behind the interface: **clear contracts, consistent state changes, inspectable results, and useful failure states**. These three projects apply those ideas in different ways.

<img src="./assets/architecture.svg" width="100%" alt="Three application blueprints: NEXORA source analysis, TalentOS bounded extraction and explainable ranking, and AegisVault policy, encryption, transactional storage, and audit" />

The [engineering walkthroughs](./docs/engineering-notes.md) connect each implementation to its design choices, tradeoffs, source revisions, and recorded verification.

## Toolbox

**Python and TypeScript** are my main tools. The rest of the stack comes from the applications linked here.

Select an icon to explore the technology. Project examples are listed below.

**Languages & foundations**

<p>
<a href="https://www.python.org/" title="Explore Python"><img src="./assets/icons/python.svg" width="80" height="90" alt="Python" /></a>
<a href="https://www.typescriptlang.org/" title="Explore TypeScript"><img src="./assets/icons/typescript.svg" width="80" height="90" alt="TypeScript" /></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" title="Explore JavaScript"><img src="./assets/icons/javascript.svg" width="80" height="90" alt="JavaScript" /></a>
<a href="https://dev.java/" title="Explore Java"><img src="./assets/icons/java.svg" width="80" height="90" alt="Java" /></a>
<a href="https://en.cppreference.com/w/c" title="Explore C"><img src="./assets/icons/c.svg" width="80" height="90" alt="C" /></a>
<a href="https://isocpp.org/" title="Explore C++"><img src="./assets/icons/cplusplus.svg" width="80" height="90" alt="C++" /></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/HTML" title="Explore HTML5"><img src="./assets/icons/html5.svg" width="80" height="90" alt="HTML5" /></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/CSS" title="Explore CSS3"><img src="./assets/icons/css3.svg" width="80" height="90" alt="CSS3" /></a>
</p>

**Web & APIs**

<p>
<a href="https://react.dev/" title="Explore React"><img src="./assets/icons/react.svg" width="80" height="90" alt="React" /></a>
<a href="https://vite.dev/" title="Explore Vite"><img src="./assets/icons/vite.svg" width="80" height="90" alt="Vite" /></a>
<a href="https://nodejs.org/" title="Explore Node.js"><img src="./assets/icons/nodedotjs.svg" width="80" height="90" alt="Node.js" /></a>
<a href="https://expressjs.com/" title="Explore Express"><img src="./assets/icons/express.svg" width="80" height="90" alt="Express" /></a>
<a href="https://fastapi.tiangolo.com/" title="Explore FastAPI"><img src="./assets/icons/fastapi.svg" width="80" height="90" alt="FastAPI" /></a>
<a href="https://docs.pydantic.dev/" title="Explore Pydantic"><img src="./assets/icons/pydantic.svg" width="80" height="90" alt="Pydantic" /></a>
</p>

**Databases & storage**

<p>
<a href="https://www.postgresql.org/" title="Explore PostgreSQL"><img src="./assets/icons/postgresql.svg" width="80" height="90" alt="PostgreSQL" /></a>
<a href="https://www.mongodb.com/" title="Explore MongoDB"><img src="./assets/icons/mongodb.svg" width="80" height="90" alt="MongoDB" /></a>
<a href="https://redis.io/" title="Explore Redis"><img src="./assets/icons/redis.svg" width="80" height="90" alt="Redis" /></a>
<a href="https://www.sqlite.org/" title="Explore SQLite"><img src="./assets/icons/sqlite.svg" width="80" height="90" alt="SQLite" /></a>
<a href="https://www.sqlalchemy.org/" title="Explore SQLAlchemy"><img src="./assets/icons/sqlalchemy.svg" width="80" height="90" alt="SQLAlchemy" /></a>
</p>

**Machine learning & data**

<p>
<a href="https://pytorch.org/" title="Explore PyTorch"><img src="./assets/icons/pytorch.svg" width="80" height="90" alt="PyTorch" /></a>
<a href="https://scikit-learn.org/" title="Explore scikit-learn"><img src="./assets/icons/scikitlearn.svg" width="80" height="90" alt="scikit-learn" /></a>
<a href="https://numpy.org/" title="Explore NumPy"><img src="./assets/icons/numpy.svg" width="80" height="90" alt="NumPy" /></a>
<a href="https://pandas.pydata.org/" title="Explore pandas"><img src="./assets/icons/pandas.svg" width="80" height="90" alt="pandas" /></a>
<a href="https://scipy.org/" title="Explore SciPy"><img src="./assets/icons/scipy.svg" width="80" height="90" alt="SciPy" /></a>
</p>

**Tools & delivery**

<p>
<a href="https://www.docker.com/" title="Explore Docker"><img src="./assets/icons/docker.svg" width="80" height="90" alt="Docker" /></a>
<a href="https://git-scm.com/" title="Explore Git"><img src="./assets/icons/git.svg" width="80" height="90" alt="Git" /></a>
<a href="https://github.com/" title="Explore GitHub"><img src="./assets/icons/github.svg" width="80" height="90" alt="GitHub" /></a>
<a href="https://github.com/features/actions" title="Explore GitHub Actions"><img src="./assets/icons/githubactions.svg" width="80" height="90" alt="GitHub Actions" /></a>
<a href="https://www.kernel.org/" title="Explore Linux"><img src="./assets/icons/linux.svg" width="80" height="90" alt="Linux" /></a>
<a href="https://docs.pytest.org/" title="Explore pytest"><img src="./assets/icons/pytest.svg" width="80" height="90" alt="pytest" /></a>
<a href="https://playwright.dev/" title="Explore Playwright"><img src="./assets/icons/playwright.svg" width="80" height="90" alt="Playwright" /></a>
<a href="https://docs.astral.sh/ruff/" title="Explore Ruff"><img src="./assets/icons/ruff.svg" width="80" height="90" alt="Ruff" /></a>
<a href="https://docs.astral.sh/uv/" title="Explore uv"><img src="./assets/icons/uv.svg" width="80" height="90" alt="uv" /></a>
</p>

**AI integrations**

<p>
<a href="https://platform.openai.com/docs/" title="Explore OpenAI"><img src="./assets/icons/openai.svg" width="80" height="90" alt="OpenAI" /></a>
<a href="https://docs.anthropic.com/" title="Explore Anthropic"><img src="./assets/icons/anthropic.svg" width="80" height="90" alt="Anthropic" /></a>
<a href="https://ollama.com/" title="Explore Ollama"><img src="./assets/icons/ollama.svg" width="80" height="90" alt="Ollama" /></a>
</p>

<details>
<summary><b>Stack details and where each tool appears</b></summary>

<br />

| Area | Tools | Example repositories |
| :--- | :--- | :--- |
| Frontend | React · TypeScript · Vite · HTML · CSS | NEXORA, TalentOS, Concord |
| APIs & validation | FastAPI · Pydantic · Node.js · Express · HTTPX · MCP | DevOS, NEXORA, LeafScan |
| Persistence | PostgreSQL · SQLAlchemy · Alembic · SQLite · MongoDB · optional Redis | AegisVault, TalentOS, LeafScan, URLShortener |
| ML & data | PyTorch · scikit-learn · NumPy · Pandas · SciPy · Matplotlib · Seaborn | LeafScan, candidate ranking, data-analysis projects |
| Voice & providers | Whisper · PySide6 · OpenAI · Anthropic · optional Ollama | LEXA |
| Delivery & verification | Docker · GitHub Actions · pytest · Playwright · Hypothesis · Ruff · uv | NEXORA, AegisVault, TalentOS |
| Programming foundations | Java · C · C++ · JavaScript · SQL · Verilog | Coursework, algorithms, and programming foundations |

These tools reflect project manifests, documentation, and my stated foundations. Some integrations are optional; each repository describes its implementation scope. Forks are excluded from the language graph below.

</details>

## GitHub work atlas

A connected map of my public non-fork repositories: project areas on the outside, documented tools in the middle, and primary languages at the core.

<a href="https://raw.githubusercontent.com/arpitkjaiswal/arpitkjaiswal/main/assets/work-atlas.svg"><img src="./assets/work-atlas.svg" width="100%" alt="Animated GitHub Work Atlas connecting public non-fork project repositories to their primary languages and documented tools, grouped by project area" /></a>

[**Open the full-size graph**](https://raw.githubusercontent.com/arpitkjaiswal/arpitkjaiswal/main/assets/work-atlas.svg) · [Download the interactive explorer](https://raw.githubusercontent.com/arpitkjaiswal/arpitkjaiswal/main/assets/work-atlas.html) · [Graph data](./assets/work-atlas-data.json)

Save the explorer HTML file and open it in a browser to **search, filter, pan, zoom, and inspect each connection**. It works offline; GitHub displays the animated image here.

<div align="center">

<img src="./assets/contributions.svg" width="100%" alt="Public GitHub contribution calendar with an animated light trail; each cell uses real GitHub contribution data" />

<br /><br />
<img src="./assets/languages.svg" width="49%" alt="Primary-language distribution across public non-fork repositories, with a decorative orbital accent" />
<img src="./assets/monthly.svg" width="49%" alt="Monthly GitHub contribution counts with an animated cyan and violet gradient" />

</div>

<details>
<summary><b>Data sources and graph methodology</b></summary>

<br />

- **Calendar:** contributions displayed on my public GitHub calendar. The moving light is decorative.
- **Monthly chart:** contributions grouped into the latest 12 calendar months; the current month is partial.
- **Languages:** one GitHub-detected primary language per public non-fork repository. This profile and repositories without a detected language are excluded. Counts describe repositories, not lines of code or proficiency.
- **Work atlas:** includes every public non-fork project repository, including those without a detected language. Project areas are curated; tool links come from reviewed manifests and READMEs. Links describe primary languages or documented tool use, not dependencies between repositories. Motion is decorative.
- **Updates:** the daily workflow refreshes the checked-in graphics. During GitHub HTTP outages, it warns and preserves the dated snapshot. Snapshot dates remain unchanged until fresh data is fetched successfully.

[Data snapshot](./assets/profile-data.json) · [Refresh script](./scripts/update_profile.py) · [Workflow runs](https://github.com/arpitkjaiswal/arpitkjaiswal/actions/workflows/profile-visuals.yml)

</details>

<img src="./assets/divider.svg" width="100%" alt="Animated signal divider" />

## Contact

<img src="./assets/footer.svg" width="100%" alt="Let's build something worth using. Open to software engineering opportunities and collaborations." />

Open to **software engineering roles, internships, and collaborations**, especially around developer tools, backend systems, and useful AI applications.

<p align="left">
<a href="https://www.linkedin.com/in/arpit-kumar-jaiswal-819478302"><img src="./assets/contact/linkedin.svg" width="176" alt="LinkedIn: Let’s connect" /></a>
<a href="mailto:arpit.kr.jaiswal@gmail.com"><img src="./assets/contact/email.svg" width="176" alt="Email: Say hello" /></a>
<a href="https://github.com/arpitkjaiswal?tab=repositories"><img src="./assets/contact/github.svg" width="176" alt="GitHub: Explore the code" /></a>
</p>
