"""Mem0 MCP Server — shared semantic memory for Claude Code agents.

Connects to Qdrant (vector DB) + Ollama (embeddings) + Anthropic (fact extraction)
to provide persistent, searchable memory across multiple terminals and sessions.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP(name="mem0")

# ---------------------------------------------------------------------------
# Mem0 initialization (lazy singleton)
# ---------------------------------------------------------------------------

_mem0_instance = None


def _build_config() -> dict:
    return {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "host": os.environ.get("QDRANT_HOST", "localhost"),
                "port": int(os.environ.get("QDRANT_PORT", "6333")),
                "collection_name": os.environ.get(
                    "MEM0_COLLECTION", "claude-code-memory"
                ),
                "embedding_model_dims": 768,
            },
        },
        "embedder": {
            "provider": "ollama",
            "config": {
                "model": os.environ.get("OLLAMA_MODEL", "nomic-embed-text"),
                "ollama_base_url": os.environ.get(
                    "OLLAMA_URL", "http://localhost:11434"
                ),
            },
        },
        "llm": {
            "provider": "anthropic",
            "config": {
                "model": os.environ.get("MEM0_LLM_MODEL", "claude-haiku-4-5-20251001"),
                "api_key": os.environ.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_KEY", "")),
            },
        },
    }


def get_mem0():
    """Lazy-init Mem0 client."""
    global _mem0_instance
    if _mem0_instance is None:
        from mem0 import Memory

        _mem0_instance = Memory.from_config(_build_config())
    return _mem0_instance


# ---------------------------------------------------------------------------
# Default user_id scoping
# ---------------------------------------------------------------------------

_DEFAULT_USER = os.environ.get("MEM0_USER_ID", "claude-code")


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def mem0_store(
    content: str,
    memory_type: str = "general",
    project: str = "",
    tags: str = "",
    user_id: str = "",
) -> str:
    """Store a fact, decision, procedure, or any knowledge in shared memory.

    Args:
        content: The memory content to store. Be specific and factual.
        memory_type: Type of memory — procedural, decision, project, feedback, reference, episodic, general.
        project: Project name this memory relates to (empty for cross-project).
        tags: Comma-separated tags for categorization (e.g. "architecture,python,testing").
        user_id: Memory scope/owner (defaults to MEM0_USER_ID env var).
    """
    uid = user_id or _DEFAULT_USER
    metadata = {
        "type": memory_type,
        "stored_at": datetime.now(timezone.utc).isoformat(),
    }
    if project:
        metadata["project"] = project
    if tags:
        metadata["tags"] = tags

    try:
        result = get_mem0().add(content, user_id=uid, metadata=metadata)
        count = len(result.get("results", [])) if isinstance(result, dict) else 1
        return json.dumps(
            {"status": "stored", "memories_created": count, "user_id": uid}
        )
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
async def mem0_recall(
    query: str,
    limit: int = 10,
    user_id: str = "",
) -> str:
    """Search shared memory semantically. Use before starting work to get context.

    Args:
        query: Natural language query to search memories (e.g. "how to create GitHub issues").
        limit: Maximum number of memories to return (default 10).
        user_id: Memory scope to search (defaults to MEM0_USER_ID env var).
    """
    uid = user_id or _DEFAULT_USER

    try:
        results = get_mem0().search(query, user_id=uid, limit=limit)
        memories = []

        items = results if isinstance(results, list) else results.get("results", [])
        for r in items:
            memory = {
                "content": r.get("memory", ""),
                "score": r.get("score", 0),
            }
            if meta := r.get("metadata"):
                memory["type"] = meta.get("type", "general")
                memory["project"] = meta.get("project", "")
                memory["tags"] = meta.get("tags", "")
                memory["stored_at"] = meta.get("stored_at", "")
            if mid := r.get("id"):
                memory["id"] = mid
            memories.append(memory)

        return json.dumps({"query": query, "count": len(memories), "memories": memories})
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
async def mem0_search(
    query: str,
    memory_type: str = "",
    project: str = "",
    limit: int = 10,
    user_id: str = "",
) -> str:
    """Search memory with optional filters by type and project.

    Args:
        query: Natural language search query.
        memory_type: Filter by type — procedural, decision, project, feedback, reference, episodic, general.
        project: Filter by project name.
        limit: Maximum results (default 10).
        user_id: Memory scope (defaults to MEM0_USER_ID env var).
    """
    uid = user_id or _DEFAULT_USER

    try:
        results = get_mem0().search(query, user_id=uid, limit=limit * 3)
        items = results if isinstance(results, list) else results.get("results", [])

        memories = []
        for r in items:
            meta = r.get("metadata", {})
            if memory_type and meta.get("type", "") != memory_type:
                continue
            if project and meta.get("project", "") != project:
                continue

            memory = {
                "content": r.get("memory", ""),
                "score": r.get("score", 0),
                "type": meta.get("type", "general"),
                "project": meta.get("project", ""),
                "tags": meta.get("tags", ""),
                "stored_at": meta.get("stored_at", ""),
            }
            if mid := r.get("id"):
                memory["id"] = mid
            memories.append(memory)

            if len(memories) >= limit:
                break

        return json.dumps({"query": query, "count": len(memories), "memories": memories})
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
async def mem0_list(
    user_id: str = "",
    limit: int = 50,
) -> str:
    """List all memories. Use to see what's stored.

    Args:
        user_id: Memory scope (defaults to MEM0_USER_ID env var).
        limit: Maximum memories to return (default 50).
    """
    uid = user_id or _DEFAULT_USER

    try:
        results = get_mem0().get_all(user_id=uid, limit=limit)
        items = results if isinstance(results, list) else results.get("results", [])

        memories = []
        for r in items:
            meta = r.get("metadata", {})
            memory = {
                "content": r.get("memory", ""),
                "type": meta.get("type", "general"),
                "project": meta.get("project", ""),
                "tags": meta.get("tags", ""),
                "stored_at": meta.get("stored_at", ""),
            }
            if mid := r.get("id"):
                memory["id"] = mid
            memories.append(memory)

        return json.dumps({"count": len(memories), "memories": memories})
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
async def mem0_delete(
    memory_id: str = "",
    user_id: str = "",
    delete_all: bool = False,
) -> str:
    """Delete a specific memory by ID, or all memories for a user.

    Args:
        memory_id: The ID of the memory to delete (from recall/search results).
        user_id: Memory scope (defaults to MEM0_USER_ID env var).
        delete_all: If true, deletes ALL memories for user_id. Use with caution.
    """
    uid = user_id or _DEFAULT_USER

    try:
        mem0 = get_mem0()
        if delete_all:
            mem0.delete_all(user_id=uid)
            return json.dumps({"status": "deleted_all", "user_id": uid})
        elif memory_id:
            mem0.delete(memory_id)
            return json.dumps({"status": "deleted", "memory_id": memory_id})
        else:
            return json.dumps(
                {"status": "error", "error": "Provide memory_id or set delete_all=true"}
            )
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


@mcp.tool()
async def mem0_update(
    memory_id: str,
    content: str,
) -> str:
    """Update an existing memory's content.

    Args:
        memory_id: The ID of the memory to update (from recall/search results).
        content: The new content for this memory.
    """
    try:
        get_mem0().update(memory_id, content)
        return json.dumps({"status": "updated", "memory_id": memory_id})
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
