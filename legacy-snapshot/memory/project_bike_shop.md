---
name: Projeto bike-shop
description: Projeto principal do Nelson - time de agents autônomos (Mr. Robot, Elliot, Tyrell) rodando como bots Slack via Claude Code CLI
type: project
---

## Bike Shop - Multi-Agent Team

**Localização**: `~/software_development/workoutspace/bike_shop/` (diretório com underscore)
**Repo GitHub**: `nelsonfrugeri-tech/bike-shop` (com hífen)
**Branch ativa**: `feat/improvement`
**Stack**: Python 3.11+, slack-bolt, slack-sdk, PyJWT, hatchling

### O que é
Sistema de agents autônomos que rodam como bots no Slack, cada um com persona e papel definido:

- **Mr. Robot** (Arch) — Arquiteto senior, direto e questionador. Agent key: `mr-robot`
- **Elliot Alderson** (Dev) — Dev brilhante, introvertido, obsessivo com código limpo. Agent key: `elliot`
- **Tyrell Wellick** (Tech PM) — PM ambicioso, organizado, focado em execução. Agent key: `tyrell`

### Arquitetura
- **agents.py** — PERSONAS dict com system prompts de cada agent
- **config.py** — AgentConfig dataclass, load_config(), resolve_team_mentions()
- **handlers.py** — Core: recebe mensagens Slack, chama `claude -p` via subprocess, retorna resposta. Inclui session tracking, memory persistente, GitHub App auth, MCP config
- **main.py** — CLI entrypoint: start/stop/status de agents via Socket Mode
- **bin/*.sh** — Scripts que iniciam agents usando claude CLI com agents .md do ~/.claude/agents/
- **mcp.json** — Integrações: Notion, Trello, draw.io, Excalidraw

### Como funciona
1. Cada agent tem um Slack bot com bot_token e app_token próprios
2. Quando mencionado no Slack, handlers.py chama `claude -p` com o system prompt + contexto da thread
3. Resposta é postada de volta na thread do Slack
4. Sessions são tracked por thread_ts para continuidade
5. Memory persistente em `~/.claude/workspace/bike-shop/memory/<agent_key>/MEMORY.md`

### Dois modos de execução
1. **Via bike_shop Python** (main.py) — Socket Mode, gerencia PID, start/stop/status
2. **Via bin/*.sh** — Scripts que usam `claude --append-system-prompt` com os agents .md

### Problemas conhecidos (2026-03-27)
- Agents delegam entre si excessivamente, consumindo toda a quota de tokens
- Regra 4 (parcimônia de tokens) NUNCA foi implementada nos agents .md
- Regra 2 (obrigar code review) está parcial
- Nelson é o orquestrador principal e deve validar decisões em pontos-chave

**Why:** Este é o projeto principal que o Nelson está construindo — um time de AI agents colaborativos no Slack.
**How to apply:** Sempre que Nelson mencionar "bike-shop", "os agents", "mr-robot", "elliot", "tyrell" — é sobre este projeto.
