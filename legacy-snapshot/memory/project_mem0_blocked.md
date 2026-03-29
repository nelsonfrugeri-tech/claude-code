---
name: Mem0 implementation blocked by disk space
description: Feature memory-agent-mem0 parada por falta de espaço em disco (1.2GB livre, Ollama precisa ~3GB). Branch feat/memory-agent-mem0 com código pronto.
type: project
---

## Status: BLOQUEADO — disco cheio

**Branch**: `feat/memory-agent-mem0` (código pronto, não testado)
**Blocker**: 1.2GB livre no Mac M1, Ollama precisa ~3GB pra imagem Docker
**Issue**: #4 no bike-shop

### O que está pronto no código:
- `docker-compose.yml` — Qdrant + Ollama adicionados
- `memory_agent.py` — MemoryAgent com Mem0 (observe + recall)
- `memory.py` — simplificado (backward compat wrapper)
- `slack/handler.py` — integrado (recall antes do LLM, observe depois)
- `.env.example` — vars QDRANT_HOST, QDRANT_PORT, OLLAMA_URL, ANTHROPIC_API_KEY
- `memory-agent.md` — spirit criado em ~/.claude/agents/
- `pyproject.toml` — mem0ai adicionado como dependência

### Próximos passos:
1. Otimizar disco do Mac M1 (liberar espaço)
2. Subir Qdrant + Ollama
3. Baixar modelo nomic-embed-text no Ollama (`ollama pull nomic-embed-text`)
4. Testar memory-agent com os agents do bike-shop
5. Commitar e abrir PR

### Alternativa se disco continuar cheio:
- Usar API de embeddings (OpenAI text-embedding-3-small ou Voyage) ao invés de Ollama local
- Remove necessidade de Docker pra embeddings (~$0.02/1M tokens)

**Why:** Mem0 é a solução pra memória compartilhada entre agents. Resolve o problema de agents esquecendo decisões.
**How to apply:** Quando disco estiver livre, retomar desta branch.
