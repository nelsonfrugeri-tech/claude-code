# Projeto: bike-shop

## Overview

- **Path**: `/Users/nelson.frugeri/software_development/workoutspace/bike_shop/`
- **GitHub**: https://github.com/nelsonfrugeri-tech/bike-shop
- **Branch principal**: `main`
- **Branch de melhorias**: `feat/improvement`
- **Stack**: Python 3.12, slack-bolt, slack-sdk, PyJWT, python-dotenv
- **Instalação**: `uv tool install -e .` (registrado como tool `bike-shop`)

## Descrição

Multi-agent Slack team com 3 personas do Mr. Robot powered by Claude Code CLI. Cada agente é um Slack bot com personalidade própria que usa Claude Code como backend de inteligência.

## Agentes

| Agent | Slack App | Persona | agent_key |
|-------|-----------|---------|-----------|
| Elliot Alderson | Elliot Alderson | Dev brilhante, obsessivo com clean code e segurança | elliot |
| Mr. Robot | Mr. Robot | Arquiteto sênior, direto, zero tolerância a BS | mr-robot |
| Tyrell Wellick | Tyrell Wellick | PM ambicioso, estratégico, obsessivo com execução | tyrell |

## Arquitetura

```
User @mentions bot in Slack
  → slack-bolt receives event (Socket Mode)
  → handlers.py spawns background thread
  → _call_claude() invokes `claude -p` CLI
    → with --resume (session tracking per thread)
    → with --append-system-prompt-file (MEMORY.md)
    → with --mcp-config (mcp.json with resolved env vars)
  → Response posted back to Slack channel/thread
```

### Key files

| File | Purpose |
|------|---------|
| `src/bike_shop/main.py` | Entry point, starts all 3 Slack bots |
| `src/bike_shop/handlers.py` | Core: event handling, Claude CLI calls, session tracking, async processing |
| `src/bike_shop/config.py` | AgentConfig, AGENT_REGISTRY, resolve_team_mentions() |
| `src/bike_shop/agents/` | Agent prompt files (`.md`) |
| `mcp.json` | MCP server configs with ${VAR} placeholders |
| `.env` | All secrets (tokens, keys, PEM paths) |

### Funcionalidades implementadas

1. **Session tracking** — `thread_ts → session_id` mapping em JSON, `--resume` para continuidade
2. **Persistent memory** — MEMORY.md por agente em `~/.claude/workspace/bike-shop/memory/{agent}/`
3. **Async processing** — `threading.Thread(daemon=True)`, sem timeout no subprocess
4. **Resilience** — instruções para salvar progresso antes de operações longas
5. **Team mentions** — `resolve_team_mentions()` injeta mapa de @mentions no prompt
6. **MCP integration** — Notion, Trello, draw.io, Excalidraw com env vars resolvidas do .env
7. **GitHub App identity** — JWT + installation token per agent para commits com identidade própria

### Diretórios de memória

```
~/.claude/workspace/bike-shop/memory/
├── elliot/MEMORY.md
├── mr-robot/MEMORY.md
└── tyrell/MEMORY.md
```

## Secrets (em .env)

| Variável | Descrição |
|----------|-----------|
| `{AGENT}_SLACK_BOT_TOKEN` | `xoxb-...` Bot OAuth Token |
| `{AGENT}_SLACK_APP_TOKEN` | `xapp-...` App-Level Token (Socket Mode) |
| `{AGENT}_SLACK_TEAM_ID` | Workspace ID |
| `{AGENT}_GITHUB_APP_ID` | GitHub App ID |
| `{AGENT}_GITHUB_INSTALLATION_ID` | GitHub Installation ID |
| `{AGENT}_GITHUB_PEM_PATH` | Path para PEM (`~/.ssh/bike-shop-*.pem`) |
| `NOTION_API_KEY` | Notion integration token |
| `TRELLO_API_KEY` | Trello API key |
| `TRELLO_TOKEN` | Trello user token |

## Como executar

```bash
# Todos os agentes
bike-shop

# Agente específico
bike-shop --agent elliot
bike-shop --agent mr-robot
bike-shop --agent tyrell
```

## Decisões técnicas

- **Socket Mode** (não HTTP): mais simples, não precisa de URL pública
- **`claude -p` CLI** (não API direta): aproveita todo o ecossistema Claude Code (tools, MCP, agents)
- **Threading** (não asyncio): slack-bolt é sync, threading é mais simples de integrar
- **JSON para sessions** (não DB): baixa complexidade, sessions são efêmeras (24h TTL)
- **MEMORY.md** (não vector DB): simplicidade, Claude lê markdown nativamente
- **PEMs em ~/.ssh/**: segurança, fora do repo, permissions 600
