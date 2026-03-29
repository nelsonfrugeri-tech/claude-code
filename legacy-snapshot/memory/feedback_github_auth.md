---
name: GitHub issue creation method
description: Como criar issues no GitHub — usar $GITHUB_PERSONAL_ACCESS_TOKEN via curl, não gh CLI
type: feedback
---

NUNCA usar `gh issue create` ou `gh api -X POST` — o PAT do gh CLI não tem scope de issues.

Usar SEMPRE curl com `$GITHUB_PERSONAL_ACCESS_TOKEN`:

```bash
curl -s -X POST https://api.github.com/repos/nelsonfrugeri-tech/{repo}/issues \
  -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"title": "...", "body": "..."}'
```

Também existe o GitHub App `oracle-zeroone` (GITHUB_APP_ID, GITHUB_APP_PRIVATE_KEY) mas usar o PAT é mais simples.

**Why:** O `gh` CLI autentica com um PAT diferente (github_pat_...) que tem read mas NÃO write:issues. O $GITHUB_PERSONAL_ACCESS_TOKEN (ghp_...) tem permissão total.
**How to apply:** Qualquer operação de escrita no GitHub (issues, PRs, comments) deve usar curl + $GITHUB_PERSONAL_ACCESS_TOKEN.
