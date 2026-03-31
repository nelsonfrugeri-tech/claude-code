# Code Review Checklist (TypeScript/Frontend)

Checklist de code review para TypeScript/React/Next.js. Cada item aponta para a arch-ts skill que contem os padroes completos e exemplos.

---

## Como Usar

**Para cada arquivo TypeScript/TSX modificado:**

1. Percorra as categorias abaixo sequencialmente
2. Para cada check, consulte a referencia indicada na arch-ts skill
3. Marque [x] quando item verificado
4. Se encontrar violacao, gere comentario citando:
   - O check violado
   - Severidade tipica
   - Referencia da arch-ts skill

**Severidade e indicativa.** Use bom senso baseado no contexto.

---

## 🔒 Security

### [ ] 1. Secrets e Env Vars
**Verificar:**
- Sem API keys, tokens, passwords no client-side code
- Env vars com `NEXT_PUBLIC_` apenas para dados realmente publicos
- Secrets usados apenas em Server Components ou API routes
- `.env.local` no `.gitignore`

**Severidade tipica:** 🔴 Critical
**Referencia:** [Arch-Ts - Environment Variables](../../arch-ts/references/nextjs/env-vars.md)

---

### [ ] 2. XSS Prevention
**Verificar:**
- `dangerouslySetInnerHTML` nunca usado com input de usuario sem sanitizacao
- DOMPurify ou equivalente usado quando HTML dinamico e necessario
- `href` com `javascript:` protocol bloqueado
- User-generated content escapado por padrao (React faz isso, mas verificar bypasses)

**Severidade tipica:** 🔴 Critical
**Referencia:** OWASP XSS Prevention + [Arch-Ts - Security](../../arch-ts/references/security/xss.md)

---

### [ ] 3. CSRF e Forms
**Verificar:**
- Forms com CSRF tokens quando necessario
- Server Actions com validacao de origem
- Fetch requests com credentials corretamente configurados

**Severidade tipica:** 🟠 High
**Referencia:** [Arch-Ts - Server Actions](../../arch-ts/references/nextjs/server-actions.md)

---

### [ ] 4. Authentication e Authorization
**Verificar:**
- Rotas protegidas com middleware ou layout guards
- Tokens nao armazenados em localStorage (prefira httpOnly cookies)
- Verificacao de permissoes antes de exibir dados sensiveis
- Server Components usados para dados que requerem auth

**Severidade tipica:** 🔴 Critical (rotas publicas) / 🟠 High (internas)
**Referencia:** [Arch-Ts - Auth Patterns](../../arch-ts/references/nextjs/auth.md)

---

### [ ] 5. Input Validation
**Verificar:**
- Dados de formularios validados com Zod ou equivalente
- Server Actions validam input antes de processar
- Schemas compartilhados entre client e server quando possivel
- File uploads com validacao de tipo e tamanho

**Severidade tipica:** 🟠 High
**Referencia:** [Arch-Ts - Validation](../../arch-ts/references/typescript/validation.md)

---

## ♿ Accessibility

### [ ] 6. Semantic HTML
**Verificar:**
- `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<header>`, `<footer>` usados corretamente
- `<button>` para acoes, `<a>` para navegacao (nunca `<div onClick>`)
- Headings em ordem hierarquica (h1 > h2 > h3)
- Lists (`<ul>`, `<ol>`) para conteudo em lista

**Severidade tipica:** 🟠 High
**Referencia:** [Arch-Ts - Semantic HTML](../../arch-ts/references/accessibility/semantic-html.md)

---

### [ ] 7. ARIA Labels e Roles
**Verificar:**
- Elementos interativos customizados tem `role` e `aria-label`
- Icons-only buttons tem `aria-label`
- `aria-live` para conteudo dinamico que muda
- `aria-hidden="true"` em elementos decorativos
- `aria-expanded`, `aria-selected` em menus e tabs

**Severidade tipica:** 🟠 High (elementos interativos) / 🟡 Medium (decorativos)
**Referencia:** [Arch-Ts - ARIA](../../arch-ts/references/accessibility/aria.md)

---

### [ ] 8. Keyboard Navigation
**Verificar:**
- Todos os elementos interativos acessiveis via Tab
- Tab order logico (sem `tabIndex` > 0)
- Escape fecha modais/dropdowns
- Enter/Space ativa buttons
- Arrow keys para navegacao em menus/tabs
- Focus trap em modais

**Severidade tipica:** 🟠 High
**Referencia:** [Arch-Ts - Keyboard Navigation](../../arch-ts/references/accessibility/keyboard.md)

---

### [ ] 9. Focus Management
**Verificar:**
- Focus movido para modal quando abre
- Focus retorna ao trigger quando modal fecha
- Focus visivel (outline nao removido globalmente)
- Skip links para conteudo principal
- `autoFocus` usado com cuidado (pode confundir screen readers)

**Severidade tipica:** 🟠 High (modais) / 🟡 Medium (geral)
**Referencia:** [Arch-Ts - Focus Management](../../arch-ts/references/accessibility/focus.md)

---

### [ ] 10. Color e Contrast
**Verificar:**
- Contrast ratio >= 4.5:1 para texto normal (WCAG AA)
- Contrast ratio >= 3:1 para texto grande (>18px bold, >24px)
- Informacao nao transmitida apenas por cor (icones, patterns, texto)
- Dark mode com contrast adequado

**Severidade tipica:** 🟡 Medium
**Referencia:** [Arch-Ts - Color Contrast](../../arch-ts/references/accessibility/color.md)

---

### [ ] 11. Images e Media
**Verificar:**
- Todas as imagens informativas tem `alt` descritivo
- Imagens decorativas tem `alt=""`
- Videos tem captions/subtitles quando possivel
- SVGs acessiveis com `role="img"` e `aria-label`

**Severidade tipica:** 🟠 High (images informativas) / 🟢 Low (decorativas)
**Referencia:** [Arch-Ts - Accessible Media](../../arch-ts/references/accessibility/media.md)

---

## ⚡ Performance

### [ ] 12. Bundle Size
**Verificar:**
- Sem imports de bibliotecas inteiras quando so precisa de uma funcao
- Dynamic imports (`next/dynamic`, `React.lazy`) para componentes pesados
- Tree-shaking funcionando (named imports, nao default de barrel files)
- Sem dependencias duplicadas (verifique com `npm ls` ou bundle analyzer)

**Severidade tipica:** 🟠 High (>50KB adicionados) / 🟡 Medium (<50KB)
**Referencia:** [Arch-Ts - Bundle Optimization](../../arch-ts/references/performance/bundle.md)

---

### [ ] 13. Render Optimization
**Verificar:**
- `React.memo` em componentes puros renderizados frequentemente
- `useMemo` para computacoes caras
- `useCallback` para callbacks passados como props
- Keys estaveis em listas (nunca array index se a lista muda)
- State no nivel correto (nao lifting desnecessario)
- Sem state updates em cascata causando re-renders multiplos

**Severidade tipica:** 🟡 Medium / 🟠 High (listas grandes, tabelas)
**Referencia:** [Arch-Ts - React Performance](../../arch-ts/references/react/performance.md)

---

### [ ] 14. Images e Assets
**Verificar:**
- `next/image` usado em vez de `<img>` (otimizacao automatica)
- Formatos modernos (WebP, AVIF) quando possivel
- `loading="lazy"` para imagens abaixo do fold
- `priority` em imagens LCP (hero, acima do fold)
- `sizes` prop correta para responsive images

**Severidade tipica:** 🟡 Medium / 🟠 High (imagens LCP)
**Referencia:** [Arch-Ts - Image Optimization](../../arch-ts/references/nextjs/images.md)

---

### [ ] 15. Data Fetching
**Verificar:**
- Data fetching no servidor quando possivel (Server Components)
- `fetch` com `cache` e `revalidate` configurados corretamente
- Sem waterfalls (parallel data fetching com `Promise.all`)
- Loading states com Suspense boundaries
- Streaming com React Server Components quando aplicavel

**Severidade tipica:** 🟠 High (waterfalls em paginas criticas) / 🟡 Medium
**Referencia:** [Arch-Ts - Data Fetching](../../arch-ts/references/nextjs/data-fetching.md)

---

### [ ] 16. Core Web Vitals
**Verificar:**
- LCP: elemento principal renderiza rapido (sem bloqueios)
- CLS: layouts estaveis (tamanhos definidos para images/ads/embeds)
- INP: interacoes respondem rapido (<200ms)
- Sem layout shifts causados por fonts, images, ou conteudo dinamico

**Severidade tipica:** 🟠 High
**Referencia:** [Arch-Ts - Core Web Vitals](../../arch-ts/references/performance/core-web-vitals.md)

---

## 🧪 Testing

### [ ] 17. Component Tests
**Verificar:**
- Componentes criticos tem testes com Testing Library
- Testes interagem como usuario (click, type, not implementation details)
- Queries acessiveis usadas (`getByRole`, `getByLabelText`, nao `getByTestId`)
- States testados (loading, error, empty, success)

**Severidade tipica:** 🔴 Critical (componentes criticos sem testes) / 🟠 High (coverage <50%)
**Referencia:** [Arch-Ts - Testing Library](../../arch-ts/references/testing/testing-library.md)

---

### [ ] 18. Hook Tests
**Verificar:**
- Hooks customizados testados com `renderHook`
- Side effects testados (API calls, subscriptions)
- Cleanup verificado (event listeners, timers)

**Severidade tipica:** 🟠 High
**Referencia:** [Arch-Ts - Hook Testing](../../arch-ts/references/testing/hooks.md)

---

### [ ] 19. E2E Tests
**Verificar:**
- Fluxos criticos cobertos (login, checkout, CRUD principal)
- Playwright ou Cypress configurado
- Tests nao frageis (sem hard waits, usar locators estaveis)
- CI pipeline roda E2E

**Severidade tipica:** 🟠 High (fluxos criticos) / 🟡 Medium
**Referencia:** [Arch-Ts - E2E Testing](../../arch-ts/references/testing/e2e.md)

---

### [ ] 20. Accessibility Tests
**Verificar:**
- axe-core integrado nos testes
- `toHaveNoViolations()` em component tests
- Testes de keyboard navigation em componentes interativos

**Severidade tipica:** 🟡 Medium
**Referencia:** [Arch-Ts - A11y Testing](../../arch-ts/references/testing/accessibility.md)

---

## ⚙️ Code Quality

### [ ] 21. TypeScript Strict
**Verificar:**
- Sem `any` (use `unknown` se tipo e realmente desconhecido)
- Sem `@ts-ignore` ou `@ts-expect-error` sem justificativa
- Generics usados corretamente
- Utility types usados onde apropriado (Partial, Pick, Omit, Record)
- Discriminated unions para state machines
- `satisfies` operator para validacao de tipos

**Severidade tipica:** 🟡 Medium (`any` em locais isolados) / 🟠 High (`any` em interfaces publicas)
**Referencia:** [Arch-Ts - TypeScript Strict](../../arch-ts/references/typescript/strict-mode.md)

---

### [ ] 22. Component Design
**Verificar:**
- Props tipadas com interface ou type (nao inline)
- Componentes < 200 linhas (senao, decomponha)
- Single Responsibility (um componente, uma responsabilidade)
- Composition sobre inheritance
- Default exports para paginas, named exports para componentes

**Severidade tipica:** 🟡 Medium / 🟠 High (componentes >300 linhas)
**Referencia:** [Arch-Ts - Component Patterns](../../arch-ts/references/react/component-patterns.md)

---

### [ ] 23. Error Handling
**Verificar:**
- Error Boundaries em rotas/layouts
- `error.tsx` files em App Router
- Fetch errors tratados com try/catch
- User-facing error messages claras
- Sentry ou equivalente para error tracking

**Severidade tipica:** 🟠 High (rotas sem error boundary) / 🟡 Medium
**Referencia:** [Arch-Ts - Error Handling](../../arch-ts/references/react/error-handling.md)

---

### [ ] 24. Naming e Conventions
**Verificar:**
- Components: PascalCase (`UserProfile`, nao `userProfile`)
- Hooks: `use` prefix (`useAuth`, nao `getAuth`)
- Files: kebab-case ou match component name
- Constants: UPPER_SNAKE_CASE
- Types/Interfaces: PascalCase com prefixo descritivo
- Boolean props: `is`, `has`, `should` prefix

**Severidade tipica:** 🟡 Medium
**Referencia:** [Arch-Ts - Naming Conventions](../../arch-ts/references/typescript/naming.md)

---

## 🏗️ Architecture

### [ ] 25. Server vs Client Components
**Verificar:**
- `"use client"` apenas onde necessario (interatividade, hooks, browser APIs)
- Dados sensiveis apenas em Server Components
- Props serializaveis entre Server e Client Components
- Nao passando funcoes como props de Server para Client Components

**Severidade tipica:** 🟠 High (`"use client"` desnecessario em arvore grande) / 🟡 Medium
**Referencia:** [Arch-Ts - Server/Client Boundary](../../arch-ts/references/nextjs/server-client-boundary.md)

---

### [ ] 26. State Management
**Verificar:**
- State local quando possivel (useState, useReducer)
- Context para state compartilhado em arvore pequena
- External store (Zustand, Jotai) para state global complexo
- URL state para filtros/paginacao (nuqs, useSearchParams)
- Sem prop drilling excessivo (>3 niveis)

**Severidade tipica:** 🟡 Medium / 🟠 High (state management errado em escala)
**Referencia:** [Arch-Ts - State Management](../../arch-ts/references/react/state-management.md)

---

### [ ] 27. Data Fetching Patterns
**Verificar:**
- Server Components para data fetching estatico/SSR
- React Server Actions para mutacoes
- SWR/TanStack Query para client-side data fetching com cache
- Sem fetch em useEffect quando Server Component e possivel
- Loading states (Suspense, loading.tsx)

**Severidade tipica:** 🟠 High (fetch em useEffect desnecessario) / 🟡 Medium
**Referencia:** [Arch-Ts - Data Fetching Patterns](../../arch-ts/references/nextjs/data-fetching.md)

---

## 🎨 Styling

### [ ] 28. Tailwind e Design System
**Verificar:**
- Classes Tailwind consistentes (nao misturar com CSS modules sem razao)
- Design tokens usados (cores do theme, nao hex hardcoded)
- Responsive design com breakpoints corretos (sm, md, lg, xl)
- Dark mode usando `dark:` variant quando aplicavel
- Spacing consistente (usar scale: 1, 2, 3, 4, nao valores arbitrarios)

**Severidade tipica:** 🟢 Low (inconsistencias menores) / 🟡 Medium (design system violation)
**Referencia:** [Arch-Ts - Styling Patterns](../../arch-ts/references/styling/tailwind.md)

---

## Resumo Rapido

**Ordem de prioridade durante review:**

1. **Security** (checks 1-5) -> Maxima prioridade
2. **Accessibility** (checks 6-11) -> Compliance e inclusao
3. **Performance** (checks 12-16) -> Core Web Vitals e UX
4. **Testing** (checks 17-20) -> Coverage e qualidade
5. **Code Quality** (checks 21-24) -> Conformidade com arch-ts skill
6. **Architecture** (checks 25-27) -> Estrutura e patterns
7. **Styling** (check 28) -> Consistencia visual

---

## Ferramentas de Apoio

Algumas verificacoes podem ser automatizadas:
```bash
# Type checking
npx tsc --noEmit

# Linting
npx eslint . --ext .ts,.tsx

# Formatting
npx prettier --check .

# Accessibility audit (CLI)
npx axe-core-cli http://localhost:3000

# Bundle analysis
npx @next/bundle-analyzer

# Lighthouse CI
npx lhci autorun

# Testing
npx vitest run

# E2E
npx playwright test

# TypeScript strict compliance
npx tsc --noEmit --strict 2>&1 | wc -l
```

**Referencia completa:** [Arch-Ts - Tooling](../../arch-ts/references/tooling/setup.md)

---

## Notas Importantes

**Este checklist e um guia, nao uma regra rigida:**
- Use bom senso baseado no contexto do projeto
- Severidades sao indicativas, nao absolutas
- Consulte sempre a arch-ts skill para padroes detalhados
- Adapte para o contexto (startup vs enterprise, prototipo vs producao)

**Para decisao final de aprovacao:**
Consulte a secao "Decisao Final" no SKILL.md principal da review-ts.
