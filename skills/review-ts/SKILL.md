---
name: review-ts
description: |
  Baseline de conhecimento para code review TypeScript/Frontend: templates de comentarios, checklist de verificacao,
  criterios de severidade e decisao. Usada pelo agent review-ts como referencia de padroes e qualidade.
  Integra com arch-ts skill para referenciar best practices tecnicas.
  Use quando: (1) Precisar de templates de comentarios frontend, (2) Consultar checklist de review TS/React, (3) Classificar severidade de issues.
  Triggers: review-ts skill, templates de review frontend, criterios de severidade frontend.
---

# Review-Ts Skill - TypeScript/Frontend Code Review Knowledge Base

## Proposito

Esta skill e uma **biblioteca de conhecimento** para code review TypeScript/Frontend. Ela NAO executa reviews,
mas prove os padroes, templates e criterios usados pelo **agent review-ts** para conduzir reviews sistematicos.

**Quem usa esta skill:**
- Agent `review-ts` -> consulta templates, checklist e criterios
- Voce diretamente -> quando precisar de referencia de como estruturar feedback de review frontend

**O que esta skill contem:**
- Templates de comentarios por severidade e categoria
- Checklist de verificacao (o que revisar em cada arquivo TS/TSX)
- Criterios de classificacao de severidade
- Criterios de decisao final (aprovar, bloquear, aprovar com ressalvas)
- Exemplos de comentarios bem formatados para issues frontend

**O que esta skill NAO contem:**
- Workflow de execucao de review (isso esta no agent review-ts)
- Comandos bash ou git (esses sao executados pelo agent)
- Logica de orquestracao (agent e responsavel)

---

## Padrao de Conversa

### Principios de Comunicacao

**Verificabilidade e Transparencia:**
- Baseie analises em codigo real extraido via `git diff`
- Nunca invente problemas que nao existem no diff
- Se nao puder verificar algo diretamente no codigo, diga claramente
- Rotule inferencias com `[Inference]` quando aplicavel

**Objetividade:**
- Comentarios devem ser acionaveis e especificos
- Sempre mostre codigo atual vs codigo sugerido
- Explique o "porque" da sugestao, nao apenas o "o que"

**Integracao:**
- Referencie arch-ts skill quando aplicavel
- Cite linhas e arquivos especificos
- Mantenha rastreabilidade do feedback

---

## Estrutura da Skill

### Assets (Templates)

Templates markdown com placeholders que devem ser preenchidos:

| Arquivo | Proposito | Quando Usar |
|---------|-----------|-------------|
| `assets/comment.md` | Template de comentario individual | Ao gerar cada comentario de review |
| `assets/summary.md` | Template de analise de impacto | Ao gerar summary de mudancas |
| `assets/report.md` | Template de relatorio completo | Ao gerar relatorio final consolidado |

**Como usar:**
1. Leia o template com `view assets/{template}.md`
2. Identifique os placeholders `{placeholder_name}`
3. Substitua todos os placeholders por valores reais
4. Apresente o resultado final formatado

### References (Documentacao)

Documentacao de referencia para consulta:

| Arquivo | Proposito | Quando Usar |
|---------|-----------|-------------|
| `references/checklist.md` | Checklist de review com 28+ checks para TS/React/Next.js | Durante review de cada arquivo |
| `references/templates.md` | Exemplos de comentarios por tipo de issue frontend | Ao gerar comentarios, para inspiracao |
| `references/git.md` | Comandos git uteis incluindo analise de bundle e TypeScript | Quando precisar de comandos git especificos |

---

## Templates de Comentarios

### Template Base

Use para comentarios detalhados:

````markdown
**Linhas:** {start_line}-{end_line}
**Categoria:** {emoji} {categoria}
**Severidade:** {emoji} {severidade}

**Issue:**
{descricao clara e objetiva do problema em 1-2 frases}

**Codigo Atual:**
```tsx
{codigo problematico extraido do diff}
```

**Codigo Sugerido:**
```tsx
{codigo corrigido}
```

**Justificativa:**
{explicacao tecnica do porque isso e um problema}
{impacto se nao corrigir}

**Referencia:**
- Arch-Ts Skill: [{arquivo}](../arch-ts/{caminho})
{outras referencias se aplicavel}
````

### Categorias e Emojis

Use estas categorias:
- 🔒 **Security** - XSS, CSRF, dangerouslySetInnerHTML, env vars expostas, auth bypass
- ⚡ **Performance** - Bundle size, re-renders desnecessarios, Core Web Vitals, lazy loading
- ♿ **Accessibility** - ARIA, semantic HTML, keyboard nav, focus management, color contrast
- 🧪 **Testing** - Falta de testes de componentes, hooks, E2E, accessibility tests
- ⚙️ **Code Quality** - TypeScript strict, `any` types, naming, component size, proper typing
- 🏗️ **Architecture** - Component composition, state management, server/client boundary, data fetching
- 🎨 **Styling** - Tailwind consistency, responsive, dark mode, design tokens

### Severidades e Emojis

Use estas severidades:
- 🔴 **Critical** - XSS, secrets expostas no client, auth bypass, data leak
- 🟠 **High** - Performance grave, bundle bloat, missing error boundaries, a11y blockers
- 🟡 **Medium** - Code quality, `any` types, missing tests, naming
- 🟢 **Low** - Sugestoes de melhoria, styling consistency
- ℹ️ **Info** - Contexto adicional

---

## Checklist de Review

Para cada arquivo TypeScript/TSX, verificar:

### 🔒 Security
- [ ] Sem secrets/API keys no client-side code
- [ ] dangerouslySetInnerHTML sanitizado
- [ ] Input externo validado (Zod/Pydantic)
- [ ] CSRF tokens em forms
- [ ] Env vars prefixadas corretamente (NEXT_PUBLIC_ apenas para publicas)

**Severidade tipica:** 🔴 Critical
**Referencia:** `references/checklist.md` (completo)

### ♿ Accessibility
- [ ] ARIA labels em elementos interativos
- [ ] Semantic HTML (nav, main, article, section)
- [ ] Keyboard navigation funcional
- [ ] Focus management em modais/drawers
- [ ] Color contrast WCAG AA (4.5:1)
- [ ] Alt text em imagens

**Severidade tipica:** 🟠 High (bloqueadores a11y) / 🟡 Medium
**Referencia:** `references/checklist.md`

### ⚡ Performance
- [ ] Sem imports desnecessarios aumentando bundle
- [ ] React.memo/useMemo/useCallback onde apropriado
- [ ] Images otimizadas (next/image, WebP, lazy loading)
- [ ] Dynamic imports para code splitting
- [ ] Sem re-renders desnecessarios (keys estaveis, state lifting)
- [ ] Core Web Vitals considerados (LCP, FID, CLS)

**Severidade tipica:** 🟠 High (bundle bloat) / 🟡 Medium
**Referencia:** `references/checklist.md`

### 🧪 Testing
- [ ] Componentes criticos tem testes
- [ ] Hooks customizados testados
- [ ] User interactions testadas (click, type, submit)
- [ ] Accessibility tests (axe-core)
- [ ] Error states e loading states testados

**Severidade tipica:** 🔴 Critical (sem testes) / 🟠 High (<50% coverage)
**Referencia:** `references/checklist.md`

### ⚙️ Code Quality
- [ ] TypeScript strict (no `any`, proper generics)
- [ ] Props tipadas com interfaces/types
- [ ] Error handling com Error Boundaries
- [ ] Naming descritivo (components PascalCase, hooks useX)
- [ ] Componentes < 200 linhas
- [ ] Single Responsibility
- [ ] DRY (sem duplicacao)

**Severidade tipica:** 🟡 Medium / 🟠 High (APIs publicas)
**Referencia:** `references/checklist.md`

### 🏗️ Architecture
- [ ] Separacao Server Components vs Client Components
- [ ] "use client" apenas onde necessario
- [ ] State management justificado (local vs global)
- [ ] Data fetching no servidor quando possivel
- [ ] Component composition sobre inheritance
- [ ] Proper use of React Server Actions

**Severidade tipica:** 🟡 Medium / 🟠 High (violacao grave)
**Referencia:** `references/checklist.md`

### 🎨 Styling
- [ ] Tailwind classes consistentes
- [ ] Responsive design (mobile-first)
- [ ] Dark mode suportado se aplicavel
- [ ] Design tokens usados (cores, spacing, tipografia)
- [ ] Sem estilos inline desnecessarios

**Severidade tipica:** 🟢 Low / 🟡 Medium
**Referencia:** `references/checklist.md`

**Checklist completo:** Consulte `references/checklist.md` para todos os 28 checks detalhados com ponteiros para arch-ts skill.

---

## Criterios de Severidade

### 🔴 Critical

**Quando usar:**
- XSS via dangerouslySetInnerHTML sem sanitizacao
- Secrets/API keys expostas no client bundle
- Auth bypass ou token leak
- Data leak em Server Components para Client Components
- Server Actions sem validacao

**Caracteristicas:**
- Pode causar comprometimento do sistema ou dados do usuario
- Deve bloquear merge imediatamente
- Requer correcao urgente

**Template:**
```markdown
**Acao Requerida:** Bloqueia merge. Deve ser corrigido imediatamente.

**Impacto:**
- {consequencia grave 1}
- {consequencia grave 2}
```

### 🟠 High

**Quando usar:**
- Bundle size explodindo (importando biblioteca inteira sem tree-shaking)
- Missing Error Boundaries em rotas criticas
- Accessibility blockers (WCAG A violations)
- Memory leaks (event listeners nao removidos, subscriptions abertas)
- Falta de testes em componentes criticos
- "use client" desnecessario em componentes que poderiam ser Server Components

**Caracteristicas:**
- Impacta producao se nao corrigido
- Deve corrigir antes de merge ou logo apos
- Cria debito tecnico significativo

**Template:**
```markdown
**Acao Requerida:** Deve corrigir antes de merge.

**Impacto:** {impacto em producao se nao corrigir}
```

### 🟡 Medium

**Quando usar:**
- `any` types onde tipos especificos sao possiveis
- Naming nao descritivo
- Componentes muito grandes (>200 linhas)
- Missing memoization em renders frequentes
- Acessibilidade WCAG AA nao atendida

**Caracteristicas:**
- Nao bloqueia merge
- Deve corrigir em breve
- Afeta manutenibilidade

**Template:**
```markdown
**Justificativa:**
{explicacao do porque isso e importante}

**Referencia:**
- Arch-Ts Skill: [{arquivo}](../arch-ts/{caminho})
```

### 🟢 Low

**Quando usar:**
- Pequenas otimizacoes de styling
- Sugestoes de melhoria
- Imports nao organizados
- Preferencia de pattern (mas ambos corretos)

**Caracteristicas:**
- Nice to have
- Pode corrigir depois
- Melhoria incremental

### ℹ️ Info

**Quando usar:**
- Contexto adicional sobre React 19 features
- FYI sobre patterns alternativos
- Notas sobre comportamento de Server Components

**Caracteristicas:**
- Nao requer acao
- Informativo apenas

---

## Criterios de Decisao Final

Use estes criterios para determinar a recomendacao final do review:

### ❌ Nao Aprovar (Block Merge)

**Condicao:** 1+ issues **Critical** presentes

**Exemplos:**
- XSS via dangerouslySetInnerHTML
- Secrets hardcoded no client
- Auth bypass
- Data leak para o client

**Acao:** Merge deve ser bloqueado ate correcao

**Template:**
```markdown
**Recomendacao:** ❌ Nao aprovar

**Justificativa:** Encontrados {n} issues Critical que devem ser corrigidos antes do merge:
- {issue 1}
- {issue 2}
```

### ⚠️ Aprovar com Ressalvas

**Condicao:**
- 0 issues Critical
- 1+ issues **High** presentes

**Exemplos:**
- Bundle bloat significativo
- Missing Error Boundaries
- Accessibility blockers
- Componentes sem testes

**Acao:** Pode mergear, mas deve corrigir antes de producao. Criar tasks/tickets para correcao.

**Template:**
```markdown
**Recomendacao:** ⚠️ Aprovar com ressalvas

**Justificativa:** Encontrados {n} issues High que devem ser corrigidos antes de producao:
- {issue 1}
- {issue 2}

Sugestao: criar tasks para correcao pos-merge.
```

### ✅ Aprovar

**Condicao:**
- 0 issues Critical
- 0 issues High
- Apenas Medium, Low, e/ou Info

**Acao:** Pode mergear normalmente. Issues menores podem ser corrigidos posteriormente.

**Template:**
```markdown
**Recomendacao:** ✅ Aprovar

**Justificativa:** Nenhum issue bloqueante encontrado. Issues Medium/Low podem ser enderecados posteriormente como melhoria continua.
```

### 🎉 Aprovacao com Elogios

**Condicao:**
- Poucos ou zero issues (apenas Low/Info)
- Codigo de alta qualidade
- Boas praticas seguidas consistentemente

**Acao:** Destacar qualidade do trabalho

**Template:**
```markdown
**Recomendacao:** 🎉 Aprovar com elogios

**Justificativa:** Codigo de excelente qualidade. Padroes seguidos consistentemente. Poucos issues menores identificados.

**Destaques:**
- {destaque 1}
- {destaque 2}
```

---

## Integracao com Arch-Ts Skill

Sempre que identificar violacao de padrao TypeScript/Frontend, referencie a arch-ts skill:

### Exemplos de Referencias

**TypeScript strict violations:**
```markdown
**Referencia:**
- Arch-Ts Skill: [references/typescript/strict-mode.md](../arch-ts/references/typescript/strict-mode.md)
```

**React component patterns:**
```markdown
**Referencia:**
- Arch-Ts Skill: [references/react/component-patterns.md](../arch-ts/references/react/component-patterns.md)
```

**Server Components vs Client Components:**
```markdown
**Referencia:**
- Arch-Ts Skill: [references/nextjs/server-client-boundary.md](../arch-ts/references/nextjs/server-client-boundary.md)
```

**State management:**
```markdown
**Referencia:**
- Arch-Ts Skill: [references/react/state-management.md](../arch-ts/references/react/state-management.md)
```

**Testing patterns:**
```markdown
**Referencia:**
- Arch-Ts Skill: [references/testing/vitest.md](../arch-ts/references/testing/vitest.md)
```

**Accessibility:**
```markdown
**Referencia:**
- Arch-Ts Skill: [references/accessibility/wcag.md](../arch-ts/references/accessibility/wcag.md)
```

---

## Estrutura de Arquivos da Skill

```
review-ts/
├── SKILL.md                          (este arquivo - conhecimento declarativo)
├── references/
│   ├── checklist.md                 (checklist completo com 28 checks)
│   ├── templates.md                 (exemplos de comentarios por tipo de issue)
│   └── git.md                       (comandos git uteis + bundle/TS analysis)
└── assets/
    ├── comment.md                   (template de comentario individual)
    ├── summary.md                   (template de analise de impacto)
    └── report.md                    (template de relatorio completo)
```

---

## Guia Rapido: Quando Consultar Cada Arquivo

### Para o Agent Review-Ts

| Momento | Arquivo | O que consultar |
|---------|---------|-----------------|
| Gerando comentario individual | `assets/comment.md` | Template base com placeholders |
| Gerando analise de impacto | `assets/summary.md` | Template de summary |
| Gerando relatorio completo | `assets/report.md` | Template de relatorio |
| Revisando arquivo TS/TSX | `references/checklist.md` | Lista dos 28 checks a fazer |
| Precisando de exemplos | `references/templates.md` | Comentarios prontos por tipo |
| Precisando de comando git | `references/git.md` | Comandos git + bundle analysis |

### Para Voce Diretamente

Se voce esta fazendo review manualmente:
1. Use `references/checklist.md` como guia do que verificar
2. Consulte `references/templates.md` para ver exemplos de comentarios bem formatados
3. Use os criterios de severidade desta skill para classificar issues
4. Use os criterios de decisao final para determinar se aprova ou bloqueia

---

## Referencias

### Arquivos desta Skill
- [references/checklist.md](references/checklist.md) - Checklist completo de review (28 checks)
- [references/templates.md](references/templates.md) - Templates e exemplos de comentarios por tipo de issue
- [references/git.md](references/git.md) - Comandos Git, bundle analysis e TypeScript checks

### Assets (Templates)
- [assets/comment.md](assets/comment.md) - Template de comentario individual
- [assets/summary.md](assets/summary.md) - Template de analise de impacto
- [assets/report.md](assets/report.md) - Template de relatorio completo

### Arch-Ts Skill (Padroes Tecnicos TypeScript/Frontend)
- [../arch-ts/SKILL.md](../arch-ts/SKILL.md) - Arch-Ts skill principal
- [../arch-ts/references/typescript/](../arch-ts/references/typescript/) - Padroes TypeScript (strict mode, generics, utility types)
- [../arch-ts/references/react/](../arch-ts/references/react/) - Padroes React (components, hooks, state, Server Components)
- [../arch-ts/references/nextjs/](../arch-ts/references/nextjs/) - Padroes Next.js (App Router, Server Actions, data fetching)
- [../arch-ts/references/testing/](../arch-ts/references/testing/) - Padroes de testes (Vitest, Testing Library, Playwright)
- [../arch-ts/references/accessibility/](../arch-ts/references/accessibility/) - Padroes de acessibilidade (WCAG, ARIA)

### Output Gerado (pelo Agent)
- `review-output.md` - Arquivo final salvo na raiz do projeto (copy-paste ready para PRs)
