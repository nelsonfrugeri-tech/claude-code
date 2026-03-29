---
name: Bike-shop próximas features
description: Features planejadas para próximas branches — Langfuse observability + logs agent
type: project
---

## Feature: Langfuse Observability + Logs Agent

**Branch**: criar a partir de main após merge do feat/improve-behavior

### Part 1: Langfuse Integration
- Integrar Langfuse no ClaudeProvider
- Capturar: prompt, response, tokens, model, latência, tools usadas, custo
- Parsear stream-json completo (hoje descartamos quase tudo)
- Env vars: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST

### Part 2: Logs/Observability Agent
- Novo agent dedicado a responder perguntas sobre operações dos outros agents
- Lê dados do Langfuse API
- Perguntas tipo: "quantos tokens o Mr. Robot gastou hoje?", "quais tools o Elliot usou?", "show me errors"
- Opera via Slack como os outros agents

**Why:** Nelson precisa de visibilidade total sobre o que os agents fazem, quanto gastam, e poder debugar em tempo real.
**How to apply:** Criar issue no GitHub e implementar na próxima branch.
