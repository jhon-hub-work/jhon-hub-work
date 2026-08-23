<h1 align="center">Jhon Buerano</h1>

<p align="center">
  <strong>AI Automation Engineer · Full Stack Developer</strong><br/>
  I build production software that removes complexity instead of adding more.
</p>

<p align="center">
  <a href="https://jhonmbuerano.netlify.app"><img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio"/></a>
  <a href="https://www.linkedin.com/in/jhon-mycho-buerano"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="mailto:bueranojhon@gmail.com"><img src="https://img.shields.io/badge/Email-1a1a1a?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
</p>

---

## About

I design and ship systems end to end — architecture, backend, frontend, deployment, and the
documentation that makes them maintainable by someone who isn't me.

My work sits at the intersection of **AI automation**, **full stack engineering**, and
**browser/desktop tooling**. The common thread is reducing moving parts: a shipped system with two
runtime dependencies beats an unshipped one with forty.

Most of what I build is **operated by real people, in production, without a developer in the loop.**

> Build software that removes complexity instead of adding more.

---

## Current Focus

| Area | What I'm doing with it |
|---|---|
| **AI Agents** | Agent loops, tool design, and orchestration for real workflows — not demos |
| **Claude Code / Anthropic API** | Agentic development workflows, MCP servers, skill and tool authoring |
| **Browser Engineering** | Chromium/Electron internals — session isolation, lifecycle, process management |
| **Full Stack Development** | Node.js services, REST design, SQLite/Turso, zero-build frontends |
| **AI Automation** | Turning manual business operations into self-healing automated systems |
| **Workflow Systems** | Inventory, ledger, and order-lifecycle engines where correctness is non-negotiable |

---

## Claude Code, In Practice

I don't use AI to autocomplete lines — I use it as a build system. Agent loops, custom skills, MCP
servers, and rendering pipelines that run unattended. This is the real usage behind the projects
below.

<p align="center">
  <img src="assets/claude-code-stats.svg" alt="Claude Code usage: 216 sessions, 50,658 messages, 56.1M tokens, 47 active days, 15-day streak, Opus 5" width="100%"/>
</p>

---

## Featured Projects

### Wave3 Collective PH — Production E-Commerce Platform & Custom CMS

A full storefront and admin CMS built from scratch for a real Philippine streetwear brand. No
Shopify, no WordPress, no templates. **Shipped to production and sold out its first product batch.**
The owner runs the entire business through the CMS daily, with no developer involved.

**Why it exists:** the business sells through GCash and bank transfer with a hand-verified payment
screenshot — a workflow hosted checkouts aren't built around. Wave3 makes it first-class: reserve
stock → upload proof → verify → approve, with a payment window that auto-expires unpaid orders and
restocks them.

**One decision worth reading:** all media lives *in the database*, not on disk or S3. The free
hosting tier's filesystem doesn't survive redeploys. Object storage is the textbook answer at
scale — at this scale it would have added a paid dependency for no gain. The deployment constraint
drove the architecture, not the other way around.

```mermaid
flowchart LR
    C["Customer UI<br/>storefront"] -->|public API| API
    A["Admin CMS<br/>cookie-authed"] -->|admin API| API
    API["Node.js + Express<br/>REST API"] --> DB[("Turso<br/>distributed SQLite")]
```

<p>
  <img src="https://img.shields.io/badge/Node.js-1a1a1a?style=flat-square&logo=node.js&logoColor=8CC84B" alt="Node.js"/>
  <img src="https://img.shields.io/badge/Express-1a1a1a?style=flat-square&logo=express&logoColor=white" alt="Express"/>
  <img src="https://img.shields.io/badge/Vanilla_JS-1a1a1a?style=flat-square&logo=javascript&logoColor=F7DF1E" alt="Vanilla JS"/>
  <img src="https://img.shields.io/badge/Turso_SQLite-1a1a1a?style=flat-square&logo=sqlite&logoColor=003B57" alt="Turso"/>
  <img src="https://img.shields.io/badge/Render-1a1a1a?style=flat-square&logo=render&logoColor=white" alt="Render"/>
</p>

**[Live site](https://wave3collectiveph.com)** · **[Case study](https://wave3-portfolio.netlify.app)** · **[Repository (private)](https://github.com/jhon-hub-work/wave3)**

<table>
  <tr>
    <td width="50%"><img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Hero-section.jpg" alt="Wave3 storefront hero"/></td>
    <td width="50%"><img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Store-page.jpg" alt="Wave3 store page"/></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/admin-dashboard.jpg" alt="Wave3 admin CMS dashboard"/></td>
    <td><img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/inventory.jpg" alt="Wave3 inventory management"/></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Payment-Verification.jpg" alt="Wave3 manual payment verification queue"/></td>
    <td><img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Order-confirmation.jpg" alt="Wave3 order confirmation"/></td>
  </tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Mobile-home.jpg" alt="Wave3 mobile home" width="30%"/>
  <img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Mobile-store.jpg" alt="Wave3 mobile store" width="30%"/>
  <img src="https://raw.githubusercontent.com/jhon-hub-work/portfolio/main/Mobile-cart.jpg" alt="Wave3 mobile cart" width="30%"/>
</p>


---

### Obsidian Browser — Workspace-First Browser for Builders

A Chromium/Electron browser that optimizes for *work* rather than consumption. Not a Chrome clone,
and deliberately **not an AI browser** — the browser layer must be excellent with the AI turned
entirely off.

**Why it exists:** every browser is built for reading the web. None are built for building things —
holding projects, context, and tools in one keyboard-first environment that remembers where you left
off and gets smarter the longer you use it.

**One decision worth reading:** the architecture is strictly layered, and **AI is the topmost layer,
never the foundation.** Workspaces get real isolation via per-workspace Chromium session partitions
(`persist:ws-<id>`) — separate cookies, logins, cache, and history — not just visual grouping. And
Knowledge only grows through *confirmed user actions*, never passive observation. That line between
ephemeral Context and durable Knowledge is the hardest constraint in the system.

```mermaid
flowchart TD
    AI["AI Provider · replaceable, cloud optional"] --> IE["Intent Engine"]
    IE --> KE["Knowledge Engine · durable, user-confirmed"]
    KE --> CE["Context Engine · per-workspace, ephemeral"]
    CE --> WS["Workspace · isolated session partition"]
    WS --> BR["Browser · the primary product"]
```

<p>
  <img src="https://img.shields.io/badge/Electron-1a1a1a?style=flat-square&logo=electron&logoColor=9FEAF9" alt="Electron"/>
  <img src="https://img.shields.io/badge/Chromium-1a1a1a?style=flat-square&logo=googlechrome&logoColor=white" alt="Chromium"/>
  <img src="https://img.shields.io/badge/Node.js-1a1a1a?style=flat-square&logo=node.js&logoColor=8CC84B" alt="Node.js"/>
  <img src="https://img.shields.io/badge/status-early_development-555555?style=flat-square" alt="Status"/>
</p>

**[Repository](https://github.com/jhon-hub-work/ObsidianBrowser)** · [Architecture](https://github.com/jhon-hub-work/ObsidianBrowser/blob/main/ARCHITECTURE.md) · [Roadmap](https://github.com/jhon-hub-work/ObsidianBrowser/blob/main/ROADMAP.md)

<table>
  <tr>
    <td width="50%"><img src="https://raw.githubusercontent.com/jhon-hub-work/ObsidianBrowser/main/docs/screenshots/home.png" alt="Obsidian Browser home"/></td>
    <td width="50%"><img src="https://raw.githubusercontent.com/jhon-hub-work/ObsidianBrowser/main/docs/screenshots/tabs.png" alt="Obsidian Browser workspace tabs"/></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/jhon-hub-work/ObsidianBrowser/main/docs/screenshots/command-palette.png" alt="Obsidian Browser command palette"/></td>
    <td><img src="https://raw.githubusercontent.com/jhon-hub-work/ObsidianBrowser/main/docs/screenshots/private-window.png" alt="Obsidian Browser private window"/></td>
  </tr>
</table>


---

### Portfolio — Conversion-First Engineering Site

A hand-built portfolio and long-form case study site. Zero framework, zero build step — the same
constraint discipline as Wave3, applied to a site whose only job is to make a technical reader
understand the work in under two minutes.

<p>
  <img src="https://img.shields.io/badge/HTML5-1a1a1a?style=flat-square&logo=html5&logoColor=E34F26" alt="HTML5"/>
  <img src="https://img.shields.io/badge/CSS3-1a1a1a?style=flat-square&logo=css3&logoColor=1572B6" alt="CSS3"/>
  <img src="https://img.shields.io/badge/Vanilla_JS-1a1a1a?style=flat-square&logo=javascript&logoColor=F7DF1E" alt="Vanilla JS"/>
  <img src="https://img.shields.io/badge/Netlify-1a1a1a?style=flat-square&logo=netlify&logoColor=00C7B7" alt="Netlify"/>
</p>

**[Live site](https://jhonmbuerano.netlify.app)**

---


## All Public Repositories

| Repository | What it is | Stack |
|---|---|---|
| **[ObsidianBrowser](https://github.com/jhon-hub-work/ObsidianBrowser)** | Workspace-first Chromium browser for builders. Local-first, per-workspace session isolation, network-level ad blocking. | Electron · Chromium · Node.js |
| **[portfolio](https://github.com/jhon-hub-work/portfolio)** · [live](https://jhonmbuerano.netlify.app) | Conversion-first portfolio and long-form Wave3 engineering case study. No framework, no build step, no dependencies. | HTML · CSS · Vanilla JS · Netlify |
| **[jhon-hub-work](https://github.com/jhon-hub-work/jhon-hub-work)** | This profile README. | Markdown |

**Private:** `wave3` — production e-commerce platform and custom CMS, live and operated daily by a
non-technical owner. Source is closed; the [case study](https://jhonmbuerano.netlify.app) and the
screenshots above cover the architecture and the decisions.

**Also working in:** [hyperframes](https://github.com/jhon-hub-work/hyperframes) (HTML-to-video
rendering for agents) and [barehands](https://github.com/jhon-hub-work/barehands) (webcam hand
tracking as an AI interface) — forks I build on top of, not original work.

---

## How I Work

**Constraints first.** I design around the real limits — free-tier ephemeral disks, one admin user,
a non-technical operator — instead of designing for imaginary scale and paying for it immediately.

**Fewer moving parts.** Wave3 runs on two runtime dependencies. Every dependency, framework, and
service has to earn its place against the cost of operating it solo.

**Correctness where it counts.** The most valuable engineering in Wave3 wasn't a screen — it was
guaranteeing two simultaneous buyers can never purchase the same last unit. That's transactional,
tested, and boring on purpose.

**Documentation is part of the deliverable.** If a system can't be understood from its README, it
isn't finished.

---

## Toolbox

| | |
|---|---|
| **Languages** | JavaScript · Node.js · SQL · HTML · CSS |
| **Frontend** | React · vanilla JS architecture · responsive CSS · zero-build delivery |
| **Backend** | Express · REST API design · SQLite · Turso (libSQL) · PostgreSQL · session auth |
| **Desktop** | Electron · Chromium session & process model · IPC / preload isolation |
| **AI** | Claude Code · Anthropic API · OpenAI · Gemini · MCP servers · agent & tool design |
| **Automation** | n8n · Make · Zapier · workflow design |
| **Infra** | Render · Netlify · Docker · environment-driven config · custom domains + SSL |

---

<p align="center">
  <sub>Open to senior full stack, AI automation, and founding engineer roles.</sub><br/>
  <sub><a href="https://jhonmbuerano.netlify.app">Portfolio</a> · <a href="https://www.linkedin.com/in/jhon-mycho-buerano">LinkedIn</a> · <a href="mailto:bueranojhon@gmail.com">bueranojhon@gmail.com</a></sub>
</p>
