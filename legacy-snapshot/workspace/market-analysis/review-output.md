# Code Quality Review - market-analysis

**Date:** 2026-03-27
**Branch:** feature/fund-analysis-system
**Recommendation:** Approve with reservations

---

## Issue #1: Duplicate model definitions (models.py vs models/ package)

**File:** `src/market_analysis/domain/models.py` + `src/market_analysis/domain/models/`
**Severity:** HIGH
**Category:** Architecture

**Problem:**
`models.py` (171 lines) and `models/core.py` (171 lines) are byte-for-byte identical. Both define the same enums (`SeriesCode`, `CollectionStatus`, `CollectorType`, `PeriodWindow`) and the same dataclasses. Python resolves `from market_analysis.domain.models import X` to the **package** (`models/__init__.py`), so `models.py` is dead code that will silently drift.

Additionally, `models/collection.py` defines a **second** `CollectionStatus`, `CollectionResult`, `ErrorResult`, and `ValidationResult` with **incompatible signatures** from those in `models/core.py`. The CVM collector imports from `models.collection` while BCB/News collectors import from `models` (re-exports from `models.core`). These are different types with the same name.

Concrete incompatibilities:
- `core.CollectionResult`: fields `collector_type`, `collected_at`, `items_count`, `duration_seconds`, `status`
- `collection.CollectionResult`: fields `source`, `status`, `records`, `errors`, `started_at`, `finished_at`, `metadata`
- `core.ErrorResult`: fields `collector_type`, `attempted_at`, `error`, `attempts`, `status`
- `collection.ErrorResult`: fields `source`, `error_type`, `message`, `timestamp`, `details`, `recoverable`
- `core.CollectionStatus` has `SUCCESS/PARTIAL/FAILURE`; `collection.CollectionStatus` has `SUCCESS/PARTIAL/ERROR/SKIPPED`

**Fix:**
1. Delete `models.py` (the file, not the package).
2. Consolidate into a single set of result types.

---

## Issue #2: Duplicate BaseCollector protocols

**File:** `src/market_analysis/domain/interfaces.py` + `src/market_analysis/domain/models/interfaces.py`
**Severity:** HIGH
**Category:** Architecture

**Problem:**
Two `BaseCollector` protocols with incompatible signatures:
- `domain/interfaces.py::BaseCollector.collect(start_date, end_date)` returns `CollectionResult | ErrorResult` (from core)
- `domain/models/interfaces.py::BaseCollector.collect()` returns `CollectionResult` (from collection module, no args)

The BCB and News collectors implement the first. The CVM `AsyncCVMCollector` implements the second. Neither satisfies the other.

**Fix:** Choose one protocol. The parametric version is more flexible. Adapt `AsyncCVMCollector` to match.

---

## Issue #3: Duplicate entity definitions (Pydantic vs dataclass)

**File:** `src/market_analysis/domain/models/entities.py`
**Severity:** MEDIUM
**Category:** Redundant State

**Problem:**
`entities.py` defines Pydantic `FundMetadata` and `PerformanceReport` that shadow the dataclass versions in `core.py`. The `models/__init__.py` re-exports the dataclass `FundMetadata` from `core`, making the Pydantic version dead code. The comment "Legacy entities (Pydantic-based)" signals intent to remove but they are still exported.

**Fix:** Remove the Pydantic duplicates or clearly separate roles.

---

## Issue #4: Dual database layer (sync + async, no shared abstraction)

**File:** `src/market_analysis/infrastructure/database.py` (async) + `src/market_analysis/infrastructure/database/connection.py` (sync)
**Severity:** MEDIUM
**Category:** Redundant State

**Problem:**
Two independent database layers duplicating PRAGMA setup. No guarantee `sql/schema.sql` matches inline `SCHEMA_DDL`. The sync `DatabaseManager` is not used by any repository.

**Fix:** Keep `database.py` (async, used by repositories). Remove or clearly scope the sync version for scripts only.

---

## Issue #5: Duplicate NewsItem definitions

**File:** `src/market_analysis/infrastructure/news_fetcher.py` + `src/market_analysis/domain/models.py`
**Severity:** MEDIUM
**Category:** Redundant State

**Problem:**
`news_fetcher.py` defines its own `NewsItem` dataclass (field `pub_date`) while domain has `NewsItem` (field `published_at`). Same concept, different field names.

**Fix:** Use domain `NewsItem` everywhere.

---

## Issue #6: Duplicate BCB fetch logic (async vs sync)

**File:** `src/market_analysis/infrastructure/bcb_collector.py` + `src/market_analysis/infrastructure/benchmark_fetcher.py`
**Severity:** MEDIUM
**Category:** Copy-Paste Variation

**Problem:**
Both fetch from `BCB_SGS_URL` (defined in both). `bcb_collector.py` uses httpx async; `benchmark_fetcher.py` uses urllib sync. Same URL pattern, same JSON parsing, different error handling. Series code constants diverge (11 vs 432 for SELIC -- actually different series).

**Fix:** Extract shared URL builder. Consider consolidating into one module.

---

## Issue #7: Duplicate _NoCloseClient class

**File:** `bcb_collector.py` (317-327) + `news_collector.py` (266-276)
**Severity:** LOW
**Category:** Copy-Paste Variation

Identical class in both files. Extract to shared `infrastructure/http.py`.

---

## Issue #8: Leaky abstraction in performance.py

**File:** `src/market_analysis/application/performance.py` line 14
**Severity:** MEDIUM
**Category:** Leaky Abstraction

**Problem:**
Application layer imports `BenchmarkRates` (`TypeAlias = dict[str, float]`) from infrastructure. Accesses with string keys `"selic"`, `"cdi"`, `"ipca"` -- no compile-time safety.

**Fix:** Define domain-level `BenchmarkData` dataclass with typed fields.

---

## Issue #9: Magic strings and stringly-typed patterns

**Severity:** MEDIUM
**Category:** Stringly-Typed Code

- `performance.py:103-105`: `benchmarks.get("selic", 0.0)` etc.
- `benchmark_fetcher.py:114-144`: untyped dict keys
- `NU_RESERVA_CNPJ` hardcoded in 3 places (`cvm_collector.py`, `database.py` SEED_DATA, `config.py`)
- `performance.py:125`: trend as string `"up"/"down"/"flat"` -- should be enum
- `repositories.py:282`: `datetime.utcnow()` -- deprecated since Python 3.12

---

## Issue #10: Root-level scripts misplaced

**File:** `setup_test.py`, `test_end_to_end.py`, `test_schema_integration.py`, `test_smtp_only.py`, `validate_system.py`
**Severity:** LOW
**Category:** File Organization

Move test files to `tests/integration/`, scripts to `scripts/`.

---

## Issue #11: CVM month-calculation duplication

**File:** `src/market_analysis/infrastructure/cvm_collector.py`
**Severity:** LOW

The `while m <= 0: m += 12; y -= 1` pattern appears 3 times. Extract to one helper.

---

## Issue #12: CVM AsyncCVMCollector uses incompatible types

**File:** `src/market_analysis/infrastructure/cvm_collector.py` (278-365)
**Severity:** HIGH
**Category:** Broken Contract

**Problem:**
`AsyncCVMCollector.collect()` constructs `ErrorResult(source=..., error_type=...)` and `CollectionResult(source=..., records=...)` using `collection.py` variants. The domain protocol expects core.py types with completely different fields. `CollectionStatus.ERROR` from collection.py does not exist in core's enum (which has `FAILURE`).

This would fail at runtime if any orchestration code treats all collectors uniformly.

**Fix:** Consolidate types first (Issue #1), then fix the collector.

---

## Issue #13: Decimal validation discarded for float conversion

**File:** `src/market_analysis/domain/schemas_cvm.py` (71-93)
**Severity:** LOW

Validates as Decimal but `to_nav()` etc. convert to float, losing precision. For financial data, use Decimal throughout or skip the Decimal validation.

---

## Summary

| Severity | Count | Issues |
|----------|-------|--------|
| HIGH     | 3     | #1, #2, #12 |
| MEDIUM   | 5     | #3, #4, #5, #8, #9 |
| LOW      | 4     | #7, #10, #11, #13 |

**Root Cause:** Multiple contributors created parallel, incompatible versions of core types. The `domain/models/` package and `domain/models.py` coexist. Two `BaseCollector` protocols exist. Two database layers exist. The CVM collector is built against a different type system than BCB/News.

**Priority Actions:**
1. Delete `domain/models.py` (dead code shadowed by package).
2. Consolidate `models/core.py` and `models/collection.py` into one set of result types.
3. Remove duplicate `BaseCollector` -- keep `domain/interfaces.py`.
4. Fix `AsyncCVMCollector` to use consolidated types.
5. Extract `BenchmarkData` to domain, remove stringly-typed dict access.
