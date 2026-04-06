"""Tests for validate_memory_type and VALID_MEMORY_TYPES in server.py."""

import sys
import os

# Allow import without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

# Import only the pure functions — no network calls triggered
from server import VALID_MEMORY_TYPES, validate_memory_type


# ---------------------------------------------------------------------------
# VALID_MEMORY_TYPES constant
# ---------------------------------------------------------------------------


def test_valid_memory_types_contains_all_expected():
    expected = {"decision", "pattern", "outcome", "feedback", "blocker", "requirement", "context"}
    assert expected == set(VALID_MEMORY_TYPES)


def test_valid_memory_types_has_correct_length():
    assert len(VALID_MEMORY_TYPES) == 7


# ---------------------------------------------------------------------------
# validate_memory_type — happy path (all valid types)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("memory_type", [
    "decision",
    "pattern",
    "outcome",
    "feedback",
    "blocker",
    "requirement",
    "context",
])
def test_valid_types_return_true(memory_type):
    assert validate_memory_type(memory_type) is True


# ---------------------------------------------------------------------------
# validate_memory_type — invalid types
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("memory_type", [
    "fact",           # old type, not in new list
    "general",        # old default
    "preference",     # old type
    "procedure",      # old type
    "DECISION",       # case-sensitive: uppercase
    "Decision",       # mixed case
    "decision ",      # trailing space
    " decision",      # leading space
    "",               # empty string
    "unknown",        # arbitrary unknown
])
def test_invalid_types_return_false(memory_type):
    assert validate_memory_type(memory_type) is False


# ---------------------------------------------------------------------------
# validate_memory_type — non-string inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("non_string", [
    None,
    123,
    3.14,
    True,
    False,
    [],
    {},
    ("decision",),
])
def test_non_string_returns_false(non_string):
    assert validate_memory_type(non_string) is False
