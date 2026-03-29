---
name: GitHub repos mapping
description: Mapeamento dos repos GitHub da org nelsonfrugeri-tech e seus projetos correspondentes
type: reference
---

## Org: nelsonfrugeri-tech

| Repo | Projeto local | Descrição |
|---|---|---|
| `nelsonfrugeri-tech/claude-code` | `~/.claude/` | Ecossistema Claude Code (agents, skills, hooks, MCP) |
| `nelsonfrugeri-tech/bike-shop` | `~/software_development/workoutspace/bike_shop/` | Multi-agent team (Mr. Robot, Elliot, Tyrell) como bots Slack |
| `nelsonfrugeri-tech/market-analysis` | — | Generative AI Design Patterns |
| `nelsonfrugeri-tech/ai-gateway` | — | AI API Gateway |

## Git remote do .claude/

- Origin: `git@github.com:nelsonfrugeri-tech/dev-in-the-loop.git` (NOTA: repo name no GitHub é `claude-code`, remote local aponta pra `dev-in-the-loop` — pode estar desatualizado)

## Auth

- Account: `nelsonfrugeri-tech`
- Token type: PAT (keyring)
- Missing scope: `repo` (necessário para criar issues) — rodar `gh auth refresh --scopes repo`
