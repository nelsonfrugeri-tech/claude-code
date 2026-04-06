"""Unit tests for mem0 memory type validation (issue #48).

Tests run without Qdrant or Ollama — mocks the embed function and Qdrant client.
"""
import json
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Patch external dependencies before importing server
# ---------------------------------------------------------------------------

# Stub qdrant_client module
qdrant_stub = types.ModuleType("qdrant_client")
models_stub = types.ModuleType("qdrant_client.models")

for name in ("Distance", "FieldCondition", "Filter", "MatchValue", "PointStruct", "VectorParams"):
    setattr(models_stub, name, MagicMock(name=name))

qdrant_stub.QdrantClient = MagicMock(name="QdrantClient")
qdrant_stub.models = models_stub
sys.modules["qdrant_client"] = qdrant_stub
sys.modules["qdrant_client.models"] = models_stub

# Stub mcp module
mcp_stub = types.ModuleType("mcp")
server_stub = types.ModuleType("mcp.server")
fastmcp_stub = types.ModuleType("mcp.server.fastmcp")

class _FakeFastMCP:
    def __init__(self, **_kw):
        pass
    def tool(self):
        def decorator(fn):
            return fn
        return decorator
    def run(self, **_kw):
        pass

fastmcp_stub.FastMCP = _FakeFastMCP
sys.modules["mcp"] = mcp_stub
sys.modules["mcp.server"] = server_stub
sys.modules["mcp.server.fastmcp"] = fastmcp_stub

# Stub httpx
httpx_stub = types.ModuleType("httpx")
httpx_stub.Client = MagicMock(name="Client")
sys.modules["httpx"] = httpx_stub

# ---------------------------------------------------------------------------
# Now import the server module
# ---------------------------------------------------------------------------

import importlib
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mcp", "mem0-server"))
server = importlib.import_module("server")

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestValidMemoryTypes(unittest.TestCase):
    def test_valid_types_set_has_all_seven(self):
        expected = {"decision", "pattern", "outcome", "feedback", "blocker", "requirement", "context"}
        self.assertEqual(server.VALID_MEMORY_TYPES, expected)


class TestMem0StoreValidation(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_type_returns_error(self):
        result = json.loads(await server.mem0_store(content="test", memory_type="general"))
        self.assertEqual(result["status"], "error")
        self.assertIn("general", result["error"])
        self.assertIn("valid_types", result)
        self.assertEqual(sorted(result["valid_types"]), sorted(server.VALID_MEMORY_TYPES))

    async def test_invalid_type_does_not_call_embed(self):
        with patch.object(server, "embed", side_effect=Exception("should not be called")) as mock_embed:
            result = json.loads(await server.mem0_store(content="test", memory_type="bogus"))
            self.assertEqual(result["status"], "error")
            mock_embed.assert_not_called()

    async def test_valid_type_calls_embed(self):
        mock_qdrant = MagicMock()
        mock_qdrant.upsert = MagicMock()
        with patch.object(server, "embed", return_value=[0.1] * 768), \
             patch.object(server, "get_qdrant", return_value=mock_qdrant):
            result = json.loads(await server.mem0_store(content="test content", memory_type="decision"))
            self.assertEqual(result["status"], "stored")
            self.assertIn("id", result)

    async def test_all_valid_types_accepted(self):
        mock_qdrant = MagicMock()
        mock_qdrant.upsert = MagicMock()
        with patch.object(server, "embed", return_value=[0.1] * 768), \
             patch.object(server, "get_qdrant", return_value=mock_qdrant):
            for t in server.VALID_MEMORY_TYPES:
                result = json.loads(await server.mem0_store(content="test", memory_type=t))
                self.assertEqual(result["status"], "stored", f"Type '{t}' should be valid")


class TestMem0RecallContextTypeFilter(unittest.IsolatedAsyncioTestCase):
    def _make_point(self, content="mem", score=0.9, mem_type="decision"):
        point = MagicMock()
        point.id = "abc-123"
        point.score = score
        point.payload = {"content": content, "type": mem_type, "project": "", "tags": "", "stored_at": ""}
        return point

    async def test_no_type_filter_passes_none_as_should(self):
        mock_qdrant = MagicMock()
        mock_result = MagicMock()
        mock_result.points = []
        mock_qdrant.query_points = MagicMock(return_value=mock_result)

        filter_calls = []
        real_filter_cls = server.Filter

        def capturing_filter(*args, **kwargs):
            filter_calls.append(kwargs)
            return MagicMock()

        with patch.object(server, "embed", return_value=[0.1] * 768), \
             patch.object(server, "get_qdrant", return_value=mock_qdrant), \
             patch.object(server, "Filter", side_effect=capturing_filter):
            await server.mem0_recall_context(query="test", agent="neo", project="proj")

        self.assertEqual(len(filter_calls), 3, "Expected Filter called once per scope")
        for kwargs in filter_calls:
            self.assertIsNone(kwargs.get("should"), "should must be None when memory_types not set")

    async def test_type_filter_populates_should(self):
        mock_qdrant = MagicMock()
        mock_result = MagicMock()
        mock_result.points = []
        mock_qdrant.query_points = MagicMock(return_value=mock_result)

        filter_calls = []

        def capturing_filter(*args, **kwargs):
            filter_calls.append(kwargs)
            return MagicMock()

        with patch.object(server, "embed", return_value=[0.1] * 768), \
             patch.object(server, "get_qdrant", return_value=mock_qdrant), \
             patch.object(server, "Filter", side_effect=capturing_filter):
            result = json.loads(await server.mem0_recall_context(
                query="test", agent="neo", project="proj", memory_types="decision,outcome"
            ))

        self.assertIn("scopes", result)
        self.assertEqual(len(filter_calls), 3, "Expected Filter called once per scope")
        for kwargs in filter_calls:
            should = kwargs.get("should")
            self.assertIsNotNone(should, "should must be set when memory_types provided")
            self.assertEqual(len(should), 2, "Two type conditions for 'decision,outcome'")


if __name__ == "__main__":
    unittest.main()
