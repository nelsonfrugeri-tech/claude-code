---
name: Bike-shop v2 - plano de reestruturação dos agents
description: Plano aprovado pelo Nelson para reestruturar agents do bike-shop com multi-skills, model switching e novo processo de time
type: project
---

## Reestruturação bike-shop (branch feat/improve-behavior)

### Decisões validadas pelo Nelson (2026-03-27)

**Skills multi-disciplinares (todos fazem tudo, com pesos):**
- Mr. Robot: peso ARCH > CODE > AI Eng > Negócio
- Elliot: peso CODE > ARCH > AI Eng > Negócio
- Tyrell: peso NEGÓCIO > CODE > AI Eng > ARCH
- Todos são coders natos, pragmáticos, experimentais

**Nelson é o gerente/orquestrador/patrocinador:**
- Direciona, valida, decide
- Agents têm autonomia mas a partir da orquestração do Nelson
- Nelson é técnico E entende de negócio

**Regra de 5 interações entre agents:**
- Máximo 5 mensagens entre agents por thread
- Se não resolver em 5, param e marcam Nelson
- Precisam ser pragmáticos, resolver rápido, codar ao invés de discutir

**Fluxo de marcação entre agents:**
- Elliot → Mr.Robot: code review, decisão técnica
- Elliot/Mr.Robot → Tyrell: decisão de negócio
- Tyrell → Mr.Robot: decisão tech
- Todos revisam tudo (time pequeno)

**Model switching por variante de agent:**
- `mr-robot-opus.md` (opus+thinking) — pensamento profundo
- `mr-robot-sonnet.md` (sonnet) — execução/dev
- `elliot-alderson-opus.md` / `elliot-alderson-sonnet.md`
- `tyrell-wellick-opus.md` / `tyrell-wellick-sonnet.md`
- Não é preso a fase — Nelson pode pedir "pensem profundamente" em qualquer momento

**Modelo padrão por agent:**
- Discovery: Tyrell opus, Mr.Robot opus, Elliot sonnet+thinking
- Dev: todos sonnet

**Processo do time:**
1. Discovery: Tyrell (doc negócio) → Mr.Robot (arquitetura) → Elliot (tech) → todos revisam
2. Tyrell cria GitHub Issues
3. Os 3 atacam issues em paralelo (tasks pesadas: Elliot/Mr.Robot, simples/QA: Tyrell)
4. Testam incrementalmente → teste integrado final
5. Doc no GitHub Pages pro Nelson testar

**Ferramentas:**
- GitHub Issues para tasks (não mais Trello)
- Notion mantido para docs existentes
- GitHub Pages para documentação nova
- Manter draw.io e Excalidraw no MCP

**Arquivos a criar/alterar:**
1. MANIFEST.md — manifesto do time
2. 6 agents .md (3 agents x 2 modelos)
3. agents.py — PERSONAS alinhados
4. config.py/handlers.py — suporte a --model flag
5. mcp.json — remover Trello
6. bin/*.sh — atualizar para novo formato

**Auto-escalação de modelo (DEEP_THINK):**
- Dois gatilhos: (1) Nelson pede "pensem profundamente" → força opus, (2) Agent decide sozinho via marcador [DEEP_THINK]
- Agent escala pra opus quando: abordagem falhou 2+ vezes, testes não passam após 2 tentativas, review negativo, incerteza
- Travas: máx 2 escalações opus por thread, volta pra sonnet automaticamente depois
- Log visível no Slack: "_(pensando mais profundamente...)_"
- Se 2 escalações não resolveram → para e marca Nelson
- Implementar no handlers.py: parsear [DEEP_THINK] na resposta, re-executar com --model opus

**Why:** Nelson quer agents pragmáticos que codam ao invés de ficar discutindo, com controle de tokens e autonomia controlada.
**How to apply:** Implementar tudo na branch feat/improve-behavior, sem alterar nada fora dessa branch.
