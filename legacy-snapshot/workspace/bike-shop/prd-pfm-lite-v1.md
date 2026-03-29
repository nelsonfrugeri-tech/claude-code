# PRD: PFM Lite - Personal Finance Manager

**Autor:** Tyrell Wellick
**Data:** 2026-03-26
**Status:** Em Review
**Versao:** 1.0

---

## Problema

Investidores pessoa fisica no Brasil nao tem uma ferramenta simples e confiavel para consolidar dados de seus investimentos a partir de fontes oficiais (BCB, CVM, B3). As solucoes existentes dependem de libs abandonadas, sem licenca, ou com dependencias bloated que representam risco tecnico e legal.

**Para quem:** Investidores PF brasileiros que querem visibilidade consolidada dos seus investimentos com dados oficiais.

## Contexto

- Auditoria de libs realizada em 2026-03-26 por Elliot Alderson descartou 2 de 3 libs candidatas por riscos graves
- Unica dependencia externa aprovada: python-bcb (MIT, 52k downloads/mes, mantida ativamente)
- Decisao do time: reimplementar fetch de dados CVM/B3 internamente

---

## Solucao Proposta

Data layer que consome dados de 3 fontes oficiais brasileiras, calcula metricas de investimento, e apresenta visao consolidada.

### Fontes de Dados

| Fonte | Solucao | Dados | Dependencia |
|-------|---------|-------|-------------|
| BCB | python-bcb (lib externa) | SGS, PTAX, FOCUS | python-bcb MIT |
| CVM | Implementacao propria | Fundos, informes, carteira | Nenhuma (CSVs abertos) |
| B3 | Implementacao propria (se necessario) | Cotacoes, proventos | Nenhuma |

---

## User Stories

### Epic 1: Data Layer

**US-01: BCB via python-bcb** (P0, 2 dias)
- Consumir SGS, PTAX, FOCUS
- Retry com backoff exponencial (max 3)

**US-02: CVM fetch proprio** (P0, 5 dias)
- Encoding fallback: utf-8 > latin-1 > cp1252 > iso-8859-15
- Schema validation antes de processar
- Parser isolado atras de interface (fetch vs parse desacoplados)
- Retry com backoff exponencial

**US-03: B3** (P2, a definir)
- Condicional ao MVP

### Epic 2: Metricas

**US-04: Metricas financeiras** (P1, 3 dias)
- Sharpe, Sortino, Beta, Alpha
- pandas/numpy puro, sem deps extras
- Tolerancia vs calculo manual < 0.01

---

## Escopo

### In Scope (MVP)
- Data layer 3 fontes (BCB python-bcb, CVM proprio, B3 se necessario)
- Parsing resiliente CVM (encoding detection + schema validation)
- Metricas basicas (Sharpe, Sortino, Beta, Alpha)
- Retry + backoff todas as fontes
- Logging estruturado

### Out of Scope
- UI/Frontend
- Auth
- Real-time/streaming
- Integracao corretoras
- ML/previsoes
- Mobile

---

## Riscos Tecnicos

| Risco | Prob | Impacto | Mitigacao |
|-------|------|---------|-----------|
| CVM muda encoding | Alta | Alto | Fallback chain + chardet |
| CVM muda schema CSV | Alta | Alto | Schema validation + parser isolado + alertas |
| CVM muda URLs | Media | Alto | URLs configuraveis + health check |
| python-bcb descontinuada | Baixa | Medio | MIT, fork disponivel |
| Rate limiting | Media | Medio | Backoff + cache local |

---

## Constraints de Arquitetura

1. Parser CVM isolado atras de interface (fetch/parse desacoplados)
2. Uma unica dep externa de dados (python-bcb)
3. Zero libs sem licenca ou abandonadas
4. Metricas com pandas/numpy puro

---

## Metricas de Sucesso

| Metrica | Target |
|---------|--------|
| Fetch CVM confiavel | > 95% em 30 dias |
| Ingestao completa | < 5 min |
| Encoding coverage | 100% |
| Acuracia metricas | desvio < 0.01 |

---

## Timeline

| Fase | Periodo | Owner |
|------|---------|-------|
| PRD Review | 2026-03-26 | Time |
| Arquitetura/Design | 03-27 ~ 03-28 | Mr. Robot |
| Sprint 1: CVM | 03-29 ~ 04-04 | Elliot |
| Sprint 2: BCB | 04-05 ~ 04-09 | Elliot |
| Sprint 3: Metricas | 04-10 ~ 04-14 | Elliot |
| Sprint 4: QA | 04-15 ~ 04-18 | Time |
| MVP Ready | 2026-04-18 | - |

---

## Aprovacoes

| Papel | Nome | Status |
|-------|------|--------|
| PM | Tyrell Wellick | Aprovado |
| Arquiteto | Mr. Robot | Pendente |
| Dev/QA | Elliot Alderson | Pendente |
