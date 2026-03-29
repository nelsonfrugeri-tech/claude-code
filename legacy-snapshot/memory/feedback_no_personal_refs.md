---
name: Projetos devem ser agnósticos e globais
description: Nunca hardcodar nomes pessoais, paths ou referências específicas — usar env vars com fallback
type: feedback
---

Projetos são open source e globais. Nunca hardcodar:
- Nomes pessoais → usar env var com fallback (ex: PROJECT_LEAD_NAME)
- Paths absolutos → usar $HOME, ~, os.path.expanduser("~")
- Referências a máquinas específicas

**Why:** Qualquer developer no mundo deve poder clonar, configurar via README/.env e rodar.
**How to apply:** Sempre varrer código por referências pessoais antes de commitar. Usar env vars configuráveis com defaults sensatos.
