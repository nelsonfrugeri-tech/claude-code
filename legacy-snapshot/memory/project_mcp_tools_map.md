---
name: Mapa de MCP tools — quem tem acesso ao quê
description: Oracle e bike-shop agents têm MCP tools diferentes. Oracle precisa reiniciar pra carregar excalidraw/drawio.
type: reference
---

## MCP Tools Map (atualizado 2026-03-29)

### Oracle (eu) — ~/.claude/.mcp.json
- langfuse ✅ (query traces, metrics)
- excalidraw ✅ (NOVO — precisa reiniciar sessão pra carregar)
- drawio ✅ (NOVO — precisa reiniciar sessão pra carregar)
- memory-keeper ✅ (via settings.json permissions)

### Bike-shop agents — bike_shop/mcp.json
- memory-keeper ✅
- notion ✅
- drawio ✅
- excalidraw ✅
- langfuse ❌ (traces são enviados via código Python, não MCP)

### Pendências
- Oracle precisa reiniciar sessão pra carregar excalidraw/drawio
- Criar diagrama de arquitetura do bike-shop no Excalidraw após reinício
- Langfuse MCP keys estão hardcodadas no .mcp.json (local, não commitado)

**Why:** Precisamos saber quem tem acesso a quê pra não ficar tentando usar tools que não estão carregadas.
**How to apply:** Antes de usar uma MCP tool, verificar se está no mapa. Se não, adicionar ao .mcp.json e reiniciar.
