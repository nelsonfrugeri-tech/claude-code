---
name: Agents restructure — spirits/ and zeroone/
description: Plano aprovado para reorganizar agents em spirits/ (reutilizáveis) e zeroone/ (meta-agents do ecossistema), com isolamento de tools/MCP por projeto
type: project
---

## Decisão: reorganizar ~/.claude/agents/

### Nova estrutura

```
agents/
├── spirits/        # Reusable agent personas (usable by project bodies)
│   ├── architect, builder, debater, dev-py, executor
│   ├── explorer, review-py, slack-monitor, tech-pm
│
├── zeroone/        # System meta-agents (ecosystem only)
│   ├── oracle.md
│   ├── sentinel.md
│   └── memory-agent.md
│
└── adapters/       # (existing)
```

### Regras de isolamento

1. **Spirits** = agnósticos, reutilizáveis por qualquer body de projeto
2. **ZeroOne** = meta-agents do ecossistema, NUNCA acessíveis por bodies
3. **Tools/MCP** = NUNCA globais, sempre por projeto via `mcp.json`
4. **Bodies** herdam spirits mas NÃO herdam tools/MCPs do ecossistema

### GitHub Issue

nelsonfrugeri-tech/claude-code#7

**Why:** Hoje não há boundary entre spirits e meta-agents. Bodies de projetos (bike-shop) podem invocar Oracle/Sentinel, o que não deveria acontecer. MCPs globais vazam para projetos.
**How to apply:** Executar antes de implementar Mem0. Esta reorganização é pré-requisito para isolamento correto de memória.
