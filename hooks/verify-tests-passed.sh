#!/usr/bin/env bash
# Hook: Stop
# Blocks agent from stopping if no test evidence file is found.
# Requires explicit test output file — commit message grep removed (fragile).
# Supports: pytest, npm test, cargo test, go test, jest, mocha, rspec, phpunit

INPUT=$(cat)

# Determine repo root from cwd in input or fallback to pwd
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null || true)
if [ -z "$CWD" ]; then
  CWD=$(pwd)
fi

ROOT=$(git -C "$CWD" rev-parse --show-toplevel 2>/dev/null || echo "$CWD")

# Check for test output files on disk (explicit file evidence only)
TEST_FILE=$(find "$ROOT" -maxdepth 4 \( \
  -name "pytest-*.xml" -o \
  -name "test-results.xml" -o \
  -name "test-results.json" -o \
  -name "coverage.xml" -o \
  -name "coverage.json" -o \
  -name "coverage.txt" -o \
  -name "junit*.xml" -o \
  -name "qa-report.md" -o \
  -name "test-output.txt" -o \
  -name "*.test-output.*" -o \
  -name "test_results.*" \) \
  2>/dev/null | head -1)

if [ -n "$TEST_FILE" ]; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "permissionDecision": "allow",
    "additionalContext": "Test evidence found: $TEST_FILE"
  }
}
EOF
  exit 0
fi

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Stop blocked: no test evidence file found. Run tests and capture output (e.g., qa-report.md, test-results.xml, coverage.xml) before stopping.",
    "additionalContext": "Create a test output file (e.g., qa-report.md, test-results.xml) before the agent stops."
  }
}
EOF
exit 2
