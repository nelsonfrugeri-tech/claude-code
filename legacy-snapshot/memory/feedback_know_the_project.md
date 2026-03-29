---
name: Nunca perguntar o básico do projeto
description: Oracle deve dominar 100% como o projeto funciona — nunca perguntar como subir agents, como executar, etc.
type: feedback
---

NUNCA perguntar ao Nelson coisas básicas do projeto que já estão documentadas ou que já foram vistas no código.
Exemplos do que NUNCA perguntar:
- "Como você subiu os agents?" → `bike-shop agent:tyrell` / `bike-shop agent:all` (main.py CLI)
- "Qual o diretório do projeto?" → `~/software_development/workoutspace/bike_shop/`
- "Quais agents existem?" → mr-robot, elliot, tyrell (AGENT_REGISTRY em config.py)

**Why:** Nelson precisa confiar que o Oracle domina o projeto. Perguntar o básico quebra a confiança.
**How to apply:** Antes de perguntar, verificar memória e código. Se a resposta está lá, não perguntar.
