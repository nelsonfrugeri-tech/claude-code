---
name: Nunca hardcodar paths pessoais
description: Projetos são públicos — nunca usar paths absolutos como /Users/nelson.frugeri, usar $HOME ou env vars
type: feedback
---

NUNCA hardcodar paths pessoais (ex: `/Users/nelson.frugeri`) em código de projetos.
Usar `$HOME`, `~`, `os.path.expanduser("~")`, ou env vars.

**Why:** Todos os projetos são para exposição global (repos públicos). Paths hardcodados quebram portabilidade e expõem info pessoal.
**How to apply:** Antes de commitar, sempre varrer o código com grep por paths absolutos pessoais.
