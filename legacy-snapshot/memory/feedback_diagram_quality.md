---
name: Qualidade de diagramas — estado da arte
description: Diagramas devem ser elegantes, com ícones nativos, cores pastel, protocolos em edges, e revisão iterativa antes de entregar
type: feedback
---

Diagramas precisam ser nota 10000/10 — estado da arte, apresentáveis com orgulho.

**Why:** Nelson apresenta esses diagramas externamente. Qualidade medíocre é inaceitável. O primeiro diagrama ficou nota 4/10 (formatação quebrada, dark theme ruim, sem detalhes de acesso).

**How to apply:**
- Usar shapes/ícones nativos do draw.io (Person, Cloud, Hexagon, Cylinder, Server, Gateway, StoredData, Robot) — NUNCA só retângulos arredondados
- Paleta pastel elegante (lavender, sky, mint, peach, violet, rose) — NÃO dark theme
- TODA edge deve ter label de protocolo (WebSocket, subprocess, gRPC, HTTP REST, stdio, HTTPS, TCP)
- Mostrar QUEM acessa O QUÊ por QUAL protocolo — distribuição explícita de acessos
- Espaçamento generoso, alinhamento limpo, hierarquia visual clara
- Revisar iterativamente (build → inspect → ajustar) antes de entregar
- Usar um "judge" mental: perguntar "isso está nota 10000/10?" antes de mostrar ao Nelson
- Fundo branco, tipografia limpa, shadows suaves
