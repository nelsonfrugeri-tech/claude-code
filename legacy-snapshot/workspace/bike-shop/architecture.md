# pfm-lite — Architecture Design Doc v2

**Package:** `market_analysis`
**Repo:** `nelsonfrugeri-tech/pfm-lite`
**Author:** Mr. Robot
**Date:** 2026-03-27
**Status:** Ready for Implementation

---

## Package Structure

```
market_analysis/
├── __init__.py          # Public API re-exports
├── _types.py            # FetchResult, Metadata, FetchError
├── _exceptions.py       # SourceUnavailableError, ParseError, SchemaError
├── bcb/
│   ├── __init__.py      # Public: fetch_series(), list_series()
│   └── _client.py       # Thin wrapper around python-bcb
├── cvm/
│   ├── __init__.py      # Public: fetch_daily_funds(), fetch_fund_info()
│   ├── _client.py       # HTTP download only (ZIP/CSV). No parsing.
│   ├── _parser.py       # Pure transform: bytes → DataFrame. No I/O.
│   └── _schema.py       # Column schemas per CSV type + validation
├── b3/
│   ├── __init__.py      # Public: fetch_index(), fetch_historical()
│   └── _client.py       # HTTP + parse
└── metrics/
    ├── __init__.py      # Public: sharpe(), sortino(), beta(), alpha()
    └── _calc.py         # Pure pandas/numpy calculations
```

## Core Types

### _types.py

```python
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd


@dataclass(frozen=True)
class FetchError:
    code: str       # "HTTP_ERROR", "PARSE_ERROR", "PARTIAL_DATA", "SCHEMA_MISMATCH"
    message: str
    source: str     # "bcb", "cvm", "b3"
    detail: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Metadata:
    source: str
    codes: tuple[str, ...]
    start_date: str | None = None
    end_date: str | None = None
    fetched_at: datetime = field(default_factory=datetime.now)
    extra: dict = field(default_factory=dict)


@dataclass
class FetchResult:
    data: pd.DataFrame
    metadata: Metadata
    errors: list[FetchError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def __bool__(self) -> bool:
        return not self.data.empty

    def raise_on_error(self) -> "FetchResult":
        if self.errors:
            msgs = "; ".join(e.message for e in self.errors)
            raise RuntimeError(f"Fetch errors: {msgs}")
        return self

    def __repr__(self) -> str:
        return f"FetchResult(source={self.metadata.source!r}, rows={len(self.data)}, errors={len(self.errors)})"
```

### _exceptions.py

```python
class MarketAnalysisError(Exception):
    """Base exception."""

class SourceUnavailableError(MarketAnalysisError):
    """Source returned non-200 after all retries exhausted."""

class ParseError(MarketAnalysisError):
    """Failed to parse response data."""

class SchemaError(MarketAnalysisError):
    """CSV columns don't match expected schema."""
```

## Module Interfaces

Functions at top level. No classes. No base class hierarchy.

### BCB (wraps python-bcb)

```python
def fetch_series(
    codes: int | list[int],
    start: str | None = None,
    end: str | None = None,
) -> FetchResult: ...

def list_series(search: str) -> pd.DataFrame: ...
```

### CVM (custom implementation)

```python
def fetch_daily_funds(
    date: str | None = None,
    fund_cnpj: str | None = None,
) -> FetchResult: ...

def fetch_fund_info() -> FetchResult: ...
```

**CVM isolation boundary** (Elliot's requirement):
- `_client.py` — HTTP only. Downloads ZIP/CSV, returns raw `bytes`. Zero parsing.
- `_parser.py` — Pure transformation. `bytes` → `DataFrame`. No I/O. Testable with fixtures.
- `_schema.py` — Schema definitions per CSV type.

**CVM encoding strategy** (Elliot's requirement):
1. `chardet.detect()` on raw bytes
2. If confidence >= 0.7 → use detected encoding
3. If confidence < 0.7 → fallback chain: utf-8 → latin-1 → cp1252 → iso-8859-15
4. If all fail → raise `ParseError`

**CVM schema validation** (Elliot's requirement):
- Schema per CSV type: expected columns, dtypes per column
- On mismatch: log warning + skip row (partial result, not hard fail)
- `SchemaError` only on complete mismatch (0 valid rows)

### B3 (custom implementation)

```python
def fetch_index(
    index: str = "IBOV",
    date: str | None = None,
) -> FetchResult: ...

def fetch_historical(year: int) -> FetchResult: ...
```

### Metrics (pandas/numpy pure)

```python
def sharpe(returns: pd.Series, risk_free: float = 0.0) -> float: ...
def sortino(returns: pd.Series, risk_free: float = 0.0) -> float: ...
def beta(returns: pd.Series, benchmark: pd.Series) -> float: ...
def alpha(returns: pd.Series, benchmark: pd.Series, risk_free: float = 0.0) -> float: ...
```

Tolerance: deviation < 0.01 vs manual calculation.

## Error & Retry Strategy

- Retry: exponential backoff, max 3 attempts (tenacity)
- On retries exhausted: raise `SourceUnavailableError`
- No cache — consumer decides
- No fallback between sources
- Partial failures are first-class (FetchResult.errors)

## Dependencies

```
market_analysis
├── pandas (required)
├── python-bcb (required, BCB module)
├── httpx (required, CVM/B3 HTTP)
├── chardet (required, CVM encoding detection)
└── tenacity (required, retry logic)
```

Dev deps: pytest, pytest-httpx, ruff

## DataFrame Standard

All fetchers return DataFrames with consistent column naming:

| Column   | Type     | Description           |
|----------|----------|-----------------------|
| date     | datetime | Reference date        |
| value    | float    | Primary numeric value |
| source   | str      | "bcb", "cvm", "b3"   |
| code     | str      | Series/fund/index ID  |

Source-specific columns are allowed (e.g., `vl_patrim_liq` for CVM funds).

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│              market_analysis                 │
│                                             │
│  __init__.py (public API re-exports)        │
│  _types.py   (FetchResult, Metadata, etc.)  │
│  _exceptions.py                             │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   bcb/   │  │   cvm/   │  │   b3/    │  │
│  │          │  │          │  │          │  │
│  │ _client  │  │ _client  │  │ _client  │  │
│  │          │  │ _parser  │  │          │  │
│  │          │  │ _schema  │  │          │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │         │
│  ┌────────────────────────────────────────┐ │
│  │           metrics/                     │ │
│  │  sharpe() sortino() beta() alpha()     │ │
│  └────────────────────────────────────────┘ │
└───────┼─────────────┼─────────────┼─────────┘
        ▼             ▼             ▼
   python-bcb    dados.cvm.gov   b3.com.br
   (PyPI)        (HTTP/ZIP)      (HTTP)
```

## Open Questions — ALL CLOSED

1. **HTTP client**: httpx. python-bcb already uses it. Zero new deps. CLOSED.
2. **CVM date filtering**: URL pattern `inf_diario_fi_{YYYYMM}.zip`. Investigate stability in Sprint 1. CLOSED.
3. **Caching**: Out of scope v1. Consumer decides. CLOSED.

## Implementation Order

1. `_types.py` + `_exceptions.py` (Elliot, day 1)
2. `cvm/_client.py` + `cvm/_parser.py` + `cvm/_schema.py` (Sprint 1, P0)
3. `bcb/_client.py` (Sprint 2, wraps python-bcb)
4. `metrics/_calc.py` (Sprint 3)
5. `b3/` (P2, conditional)
