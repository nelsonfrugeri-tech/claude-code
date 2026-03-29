# PRD — Market Analysis v1

**Projeto**: Market Analysis
**Time**: bike-shop
**Repo**: pfm-lite (GitHub)  
**Tipo**: Python library (pip install)  
**Versao**: v1.0  
**Data**: 2026-03-26  
**Owner**: Tyrell Wellick  
**Arquiteto**: Mr. Robot  
**Dev Lead**: Elliot Alderson  

---

## 1. Visao do Produto

Lib Python para fetch de dados financeiros de fontes publicas brasileiras (BCB, CVM, B3) com calculo de metricas de risco/retorno. On-demand, sem infra, sem storage no core.

**Nao e**: uma aplicacao end-to-end. Aplicacoes (bots, dashboards, APIs) sao consumidores da lib.

---

## 2. Scope & Boundaries

| In Scope (v1) | Out of Scope (v1) |
|---|---|
| Fetch BCB (via python-bcb) | Storage/persistencia |
| Fetch CVM (implementacao propria) | CLI |
| Fetch B3 (implementacao propria) | API REST |
| Metricas: Sharpe, Sortino, drawdown | Dashboard |
| Cache opcional (TTL-based) | Noticias/sentiment |
| Error handling com retry | Batch scheduler |

**Decisao fechada**: Market Analysis = LIB (time: bike-shop). Consenso unanime do time (thread #pfm-lite, 2026-03-26).

---

## 3. Arquitetura

### 3.1 Estrutura

```
market_analysis/  # repo: pfm-lite
├── core/           # Protocol, tipos (FetchResult), excecoes
├── fetchers/       # BCB, CVM, B3
├── cache/          # Opcional, TTL-based, parquet
└── metrics/        # Sharpe, Sortino, drawdown (funcoes puras)
```

### 3.2 Contrato Principal — FetchResult

```python
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

@dataclass(frozen=True, slots=True)
class FetchResult:
    data: pd.DataFrame   # colunas: date, value
    source: str           # "bcb", "cvm", "b3"
    code: str             # codigo do ativo/serie
    fetched_at: datetime  # timestamp do fetch (TTL depende disso)

    def __post_init__(self) -> None:
        missing = {"date", "value"} - set(self.data.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
```

**Decisoes no contrato**:
- frozen=True — imutavel
- slots=True — performance
- fetched_at: datetime (nao date) — TTL de 24h precisa de hora
- Metadata (source, code) fora do DataFrame — sem redundancia por row
- Validacao no __post_init__ — fail fast

### 3.3 Protocol

```python
from typing import Protocol
from datetime import date

class DataFetcher(Protocol):
    def fetch(self, code: str, start: date, end: date) -> FetchResult: ...
```

Tres implementacoes: BCBFetcher, CVMFetcher, B3Fetcher.

### 3.4 API Publica

Duas funcoes:
- fetch(code, start, end) — busca dados
- list_sources() — lista fontes disponiveis

---

## 4. Decisoes Tecnicas

| # | Decisao | Razao |
|---|---------|-------|
| 1 | Lib, nao app | Desacoplamento. App e consumidor, nao a lib |
| 2 | Protocol, nao ABC | Structural typing. Sem heranca, sem magia |
| 3 | DataFrame (date, value) | Schema minimo viavel. source/code no wrapper |
| 4 | Storage fora do core | Lib retorna dados. Consumidor persiste |
| 5 | Cache TTL opcional | BCB=24h, CVM=7d. Modulo separado |
| 6 | Retry 3x backoff exponencial | Fontes publicas caem. SourceUnavailableError tipada |
| 7 | Metrics no core | Funcoes puras: DataFrame in, numero out |
| 8 | On-demand | Lib busca quando chamam. Batch e do consumidor |
| 9 | CVM parsing isolado | Requisito. Parser atras de interface |
| 10 | python-bcb + httpx | 2 deps externas. Minimo necessario |

---

## 5. Dependencias Externas

| Lib | Uso | Licenca | Status |
|-----|-----|---------|--------|
| python-bcb | Fetch BCB | MIT | Aprovada (52k downloads/mes) |
| httpx | HTTP client (CVM/B3) | BSD-3 | Aprovada |
| pandas | DataFrames | BSD-3 | Aprovada |

Rejeitadas: tradingcomdados (sem licenca), fundspy (abandonada 2021).

---

## 6. Metricas de Risco/Retorno (v1)

- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown

Funcoes puras que recebem DataFrame e retornam float.

---

## 7. Error Handling

```python
class SourceUnavailableError(Exception):
    """Fonte externa indisponivel apos retries."""
    pass
```

- Retry: 3 tentativas com backoff exponencial
- Sem fallback magico — se caiu, lanca excecao
- Consumidor decide o que fazer com o erro

---

## 8. Proximos Passos

| # | Tarefa | Owner | Status |
|---|--------|-------|--------|
| 1 | PRD formal | Tyrell | DONE |
| 2 | Diagrama de arquitetura | Mr. Robot | DONE |
| 3 | Validar diagrama vs PRD | Mr. Robot | Pendente |
| 4 | Implementar CVM fetcher | Elliot | Aguardando design review |
| 5 | Implementar BCB fetcher | TBD | Backlog |
| 6 | Implementar B3 fetcher | TBD | Backlog |
| 7 | Implementar metrics | TBD | Backlog |
| 8 | Setup repo + CI | TBD | Backlog |

---

## 9. Referencia

- Diagrama: ~/.claude/workspace/bike-shop/bike-shop-arch.drawio
- ADR Notion: https://www.notion.so/ADR-Market-Analysis-32f4c4da08ef80bf8feaecb25af42b25
- Thread de decisoes: #pfm-lite (2026-03-26)
