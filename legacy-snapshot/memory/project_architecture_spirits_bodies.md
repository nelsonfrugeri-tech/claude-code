---
name: Arquitetura Spirits vs Bodies
description: Agents em .claude são spirits (agnósticos, reutilizáveis). Apps (Mr. Robot, Elliot, Tyrell) são bodies que usam spirits dinamicamente.
type: project
---

## Spirits vs Bodies

**Spirits** (`~/.claude/agents/`) — Agnósticos, sem vínculo a apps ou projetos.
São capacidades puras: arquitetura, code review, SRE, coding, exploração.
Nunca referenciam ferramentas específicas (Langfuse, Slack), projetos, ou apps.

**Bodies** (bike-shop apps: Mr. Robot, Elliot, Tyrell) — Usam spirits conforme necessidade.
Trocam dinamicamente: code review → review-py, arquitetura → architect, observabilidade → sentinel.
O contexto específico (Langfuse, Slack, GitHub) vem do body, não do spirit.

**Regra**: Agents em `~/.claude/agents/` NUNCA devem referenciar ferramentas, projetos ou apps específicas.
MCP tools e configurações específicas ficam no contexto da app que invoca o agent.

**Why:** Agents reutilizáveis por qualquer app/projeto. Desacoplamento total.
**How to apply:** Ao criar ou editar agents, garantir que são agnósticos. Especificidades ficam na app.
