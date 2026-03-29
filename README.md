<div align="center">

# 🧠 Claude Code

### The Foundation Layer for AI-Powered Development

[![Claude Code](https://img.shields.io/badge/Claude_Code-CLI-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![Agents](https://img.shields.io/badge/Agents-12-blue?style=for-the-badge)](#-agents-spirits)
[![Skills](https://img.shields.io/badge/Skills-5-purple?style=for-the-badge)](#-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Reusable agents (spirits) and skills that turn `~/.claude` into an intelligent development environment.**
**Any application can use them — they are provider-agnostic and project-independent.**

[Spirits & Bodies](#-spirits--bodies) · [Agents](#-agents-spirits) · [Skills](#-skills) · [Getting Started](#-getting-started) · [Memory](#-memory-keeper)

</div>

---

## 🎯 What is this?

**claude-code** is a collection of **agents** and **skills** installed in `~/.claude/` that work with [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code). It provides specialized AI capabilities covering the entire software development lifecycle — from architecture design to code review, debugging, product management, and SRE.

The key insight: agents and skills are **spirits** — agnostic, reusable capabilities that any application can invoke. Projects like [bike-shop](https://github.com/nelsonfrugeri-tech/bike-shop) create **bodies** (Slack bots, CLI tools) that dynamically assume these spirits based on the task.

---

## 👻 Spirits & Bodies

This project follows a **spirits & bodies** architecture:

```
SPIRITS (this repo — ~/.claude/)              BODIES (apps that use spirits)
┌────────────────────────────┐          ┌──────────────────────────┐
│  architect    — designs    │          │  bike-shop               │
│  dev-py       — codes     │    ←──   │    Mr. Robot  (Slack bot) │
│  review-py    — reviews   │   used   │    Elliot     (Slack bot) │
│  debater      — debates   │    by    │    Tyrell     (Slack bot) │
│  sentinel     — monitors  │          │                          │
│  tech-pm      — plans     │          │  your-app                │
│  explorer     — explores  │    ←──   │    CLI tool              │
│  builder      — deploys   │   used   │    Web API               │
│  memory-agent — remembers │    by    │    Discord bot            │
│  ...                      │          │    ...                    │
└────────────────────────────┘          └──────────────────────────┘
```

- **Spirits** (`~/.claude/agents/`) — Pure expertise. They don't know about Slack, GitHub, or any specific project. They're capabilities: architecture, code review, SRE, coding.

- **Bodies** (external apps) — The interfaces that receive user input and invoke spirits based on context. A Semantic Router can dynamically assign spirits to bodies per task.

- **Skills** (`~/.claude/skills/`) — Knowledge bases that spirits consult. SRE principles, Python architecture patterns, code review checklists, product management practices.

---

## 🤖 Agents (Spirits)

<div align="center">

| Spirit | Specialty | Model | Trigger |
|--------|-----------|-------|---------|
| 🏛️ **architect** | System design, trade-offs, diagrams | Opus | Architecture tasks |
| 🐍 **dev-py** | Python implementation, TDD, quality | Opus | Coding tasks |
| 🔍 **review-py** | Code review, PR analysis, diff comments | Opus | PR reviews |
| ⚖️ **debater** | Compare approaches, debate trade-offs | Opus | Technical debates |
| 🔭 **explorer** | Repository analysis, codebase onboarding | Opus | New projects |
| 🔧 **builder** | Local infra, Docker, deps, env setup | Sonnet | Project setup |
| 📋 **tech-pm** | User stories, backlog, roadmap, OKRs | Opus | Product decisions |
| 👁️ **sentinel** | SRE, monitoring, observability, incidents | Haiku | System health |
| 🧬 **memory-agent** | Fact extraction, shared memory management | Haiku | Automatic |
| 🔮 **oracle** | Ecosystem manager, knowledge keeper | Opus | Meta-tasks |
| 📡 **slack-monitor** | Slack agent lifecycle management | Sonnet | Agent ops |
| ⚡ **executor** | Implements skill improvements from issues | Sonnet | Skill updates |

</div>

### How spirits work

```bash
# Use a spirit directly from Claude Code
claude --agent architect
# → You're now talking to the architect spirit

# Or invoke from code via Claude CLI
claude -p "Design a notification system" --agent architect --model opus

# Spirits can be composed in pipelines
# 1. Explorer analyzes the repo
# 2. Architect designs the solution
# 3. Dev-py implements it
# 4. Review-py reviews the PR
```

### Agent Details

#### 🏛️ Architect
Software architect and tech lead. Designs systems, defines patterns, identifies flaws and risks. Thinks in trade-offs and long-term decisions. Creates architecture diagrams and guides the team technically.

#### 🐍 Dev-Py
Python developer with a strict 8-step workflow: question → research → design → test → implement → validate → review → document. Test-first, always. Consumes `context.md` from Explorer when available.

#### 🔍 Review-Py
Systematic code review between Git branches. Three modes: impact analysis, per-file review, and full report. Comments formatted for direct copy-paste into PRs. Uses severity criteria from the `review-py` skill.

#### ⚖️ Debater
Configurable personality (Socratic, Expert, Collaborative). Debates topics, researches state of the art, analyzes gaps, and creates structured issues with improvement proposals.

#### 🔭 Explorer
Starting point for any pipeline. Analyzes a repository and generates a structured `context.md` report covering architecture, contracts, infrastructure, dependencies, and quality analysis.

#### 🔧 Builder
Spins up local infrastructure automatically. Reads `context.md`, starts Docker containers, checks `.env`, installs deps, starts services, and validates with connection tests.

#### 📋 Tech-PM
Technical Product Manager. Defines what to build, prioritizes backlog, writes user stories with acceptance criteria, plans sprints/releases, manages roadmap.

#### 👁️ Sentinel
SRE and observability specialist. Monitors systems, queries traces and metrics, analyzes health, and helps with incident response. Uses the `sre-observability` skill.

#### 🧬 Memory Agent
Phantom spirit that observes conversations and extracts facts (decisions, entities, context) into shared memory. Works with Mem0 for semantic storage.

#### 🔮 Oracle
Meta-agent for the ecosystem. Manages agents, skills, MCP servers, projects, and workspaces. Central point of context and memory across sessions.

---

## 📚 Skills

Skills are **knowledge bases** that spirits consult as reference material.

<div align="center">

| Skill | Domain | Used by |
|-------|--------|---------|
| 🏗️ **arch-py** | Python architecture, patterns, type system, async, Pydantic v2 | architect, dev-py, review-py, explorer |
| 🔍 **review-py** | Code review templates, checklists, severity criteria | review-py |
| 🤖 **ai-engineer** | LLM engineering, RAG, agents, vector DBs, MLOps | dev-py, debater |
| 📋 **product-manager** | Discovery, delivery, OKRs, user stories, roadmap | tech-pm |
| 👁️ **sre-observability** | Google SRE principles, three pillars, incident response | sentinel |

</div>

### Skill Structure

```
skills/
├── arch-py/
│   ├── SKILL.md              # Core knowledge
│   └── references/           # Supporting materials
│       ├── python/
│       │   ├── async-patterns.md
│       │   ├── type-system.md
│       │   └── ...
│       └── architecture/
│           ├── clean-architecture.md
│           └── ...
├── sre-observability.md       # Single-file skill
└── ...
```

---

## 🔄 Multi-Agent Pipelines

Spirits are designed to compose into pipelines:

### Development Pipeline
```
Explorer → Architect → Dev-Py → Review-Py → Builder
  │            │           │          │          │
  analyze    design    implement   review    deploy
  repo       system     feature     PR       local
```

### Skill Improvement Pipeline
```
Debater → Executor
   │          │
  debate    implement
  topics    improvements
```

### Applications (Bodies) Pipeline
```
Slack message → Semantic Router → Spirit selection → Claude CLI → Response
                     │
                     ├── "design the API" → architect + opus
                     ├── "review PR #42"  → review-py + sonnet
                     └── "what's the status?" → (direct) + haiku
```

---

## 📁 Project Structure

```
~/.claude/
├── agents/                        # 🤖 Spirits (agent definitions)
│   ├── architect.md
│   ├── builder.md
│   ├── debater.md
│   ├── dev-py.md
│   ├── executor.md
│   ├── explorer.md
│   ├── memory-agent.md
│   ├── oracle.md
│   ├── review-py.md
│   ├── sentinel.md
│   ├── slack-monitor.md
│   ├── tech-pm.md
│   └── adapters/
│       └── slack.md               #   Slack integration adapter
│
├── skills/                        # 📚 Knowledge bases
│   ├── arch-py/                   #   Python architecture
│   ├── ai-engineer/               #   AI/ML engineering
│   ├── product-manager/           #   Product management
│   ├── review-py/                 #   Code review
│   └── sre-observability.md       #   SRE & observability
│
├── hooks/                         # ⚡ Automations
│   ├── memory-keeper-save.sh      #   Auto-save context (PreCompact/Stop)
│   ├── memory-keeper-restore.sh   #   Auto-restore context (SessionStart)
│   ├── memory-keeper-purge.sh     #   Periodic purge (cron: 15/7 days)
│   ├── run-memory-keeper.sh       #   MCP wrapper
│   ├── setup-cron.sh              #   Purge cron installer
│   └── logs/                      #   Logs (not versioned)
│
├── setup/                         # 🔧 Onboarding
│   ├── mcp-manifest.json          #   Required MCPs (declarative)
│   └── bootstrap.sh               #   Per-machine setup script
│
├── CLAUDE.md                      # 📋 Global instructions
├── settings.json                  # ⚙️ Shared settings (hooks, env)
└── .gitignore                     # 🔒 Security (blocks everything by default)
```

### Security: What is NOT versioned

The `.gitignore` blocks **everything** by default and only allows specific folders:

| Blocked | Why |
|---------|-----|
| `settings.json` env values | Machine-specific configuration |
| `~/.claude.json` | User-scoped MCPs |
| `~/mcp-data/` | Memory Keeper data (SQLite) |
| `hooks/logs/` | Execution logs |
| `workspace/` | Agent outputs per project |
| `projects/` | Claude Code sessions and auto-memory |
| `.mcp.json` | MCP server configs with API keys |

---

## 🚀 Getting Started

### Prerequisites

| Tool | Install |
|------|---------|
| ![Claude](https://img.shields.io/badge/Claude_Code-CC785C?style=flat-square&logo=anthropic&logoColor=white) | `npm install -g @anthropic-ai/claude-code` |
| ![Node](https://img.shields.io/badge/Node.js_18+-339933?style=flat-square&logo=node.js&logoColor=white) | Required for MCP servers |

### Install

```bash
# Clone into ~/.claude
git clone https://github.com/nelsonfrugeri-tech/claude-code.git ~/.claude

# Install MCP servers
bash ~/.claude/setup/bootstrap.sh

# Install purge cron (optional)
bash ~/.claude/hooks/setup-cron.sh

# Verify
bash ~/.claude/setup/bootstrap.sh --check
```

### If `~/.claude` already exists

```bash
# Backup and init
REPO_URL=git@github.com:nelsonfrugeri-tech/claude-code.git \
  bash <(curl -sL https://raw.githubusercontent.com/nelsonfrugeri-tech/claude-code/main/setup/bootstrap.sh) --init
```

### Use a spirit

```bash
# Start Claude Code with a specific spirit
claude --agent architect    # Architecture mode
claude --agent dev-py       # Python dev mode
claude --agent sentinel     # SRE/monitoring mode
claude --agent oracle       # Ecosystem management
```

---

## 🧠 Memory Keeper

Persistent memory system across Claude Code sessions.

### How it works

```
SessionStart → hook restores context from memory
     ↓
  You work with Claude (decisions, patterns, learnings)
     ↓
PreCompact/Stop → hook saves context to memory
     ↓
  Next session → context is restored automatically
```

- Data stored in `~/mcp-data/memory-keeper/` (SQLite, per machine)
- Purge policy: every **15 days**, cleans records older than **7 days**
- Backups kept: last 3

### Manual commands

```bash
# Preview what would be purged
~/.claude/hooks/memory-keeper-purge.sh --dry-run

# Force purge now
~/.claude/hooks/memory-keeper-purge.sh --force
```

---

## 🔄 Updating

```bash
cd ~/.claude && git pull && bash setup/bootstrap.sh
```

| What changed | Action needed |
|--------------|--------------|
| `agents/*.md` | None (auto-loaded) |
| `skills/**` | None (auto-loaded) |
| `CLAUDE.md` | None (auto-loaded) |
| `settings.json` | Restart Claude Code |
| `hooks/*.sh` | None (auto-executed) |
| `setup/mcp-manifest.json` | `bash ~/.claude/setup/bootstrap.sh` |

---

## 🏍️ Projects Using This Foundation

- [**bike-shop**](https://github.com/nelsonfrugeri-tech/bike-shop) — Multi-agent Slack team with Semantic Router, Mem0 memory, and Langfuse observability

---

## 🤝 Contributing

1. Create a branch: `git checkout -b feat/my-feature`
2. Add agents in `agents/`, skills in `skills/`, hooks in `hooks/`
3. **Audit for secrets/PII** before committing — no personal paths, no API keys
4. Open a PR to `main`

### Conventions

- **Agents**: one `.md` file per agent in `agents/` — must be project-agnostic
- **Skills**: folder with `SKILL.md` + `references/` in `skills/<name>/`
- **Hooks**: executable `.sh` scripts using `$HOME` (never hardcoded paths)

---

## 📄 License

MIT — use it, fork it, build your own spirits.

---

<div align="center">

**The foundation for AI-powered development teams**

[![Claude Code](https://img.shields.io/badge/Powered_by-Claude_Code-CC785C?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)

</div>
