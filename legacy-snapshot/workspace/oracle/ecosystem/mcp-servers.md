# MCP Servers Registry

## Global (all sessions)

| Server | Config Location | Command | Purpose |
|--------|----------------|---------|---------|
| **memory-keeper** | `~/.claude.json` → mcpServers | `~/.claude/hooks/run-memory-keeper.sh` | Persistent context between sessions |

## Project: /Users/nelson.frugeri (home — main session)

Config: `~/.claude.json` → projects → `/Users/nelson.frugeri` → mcpServers

| Server | Command | Env Vars | Purpose |
|--------|---------|----------|---------|
| **arxiv-mcp-server** | `uv tool run arxiv-mcp-server` | — | Search/download arXiv papers |
| **trello** | `uv tool run mcp-trello` | TRELLO_API_KEY, TRELLO_TOKEN | Trello board management |
| **notion** | `uv tool run mcp-notion` | NOTION_API_KEY | Notion pages/databases |
| **drawio** | `uv tool run drawio-mcp` | — | Create draw.io diagrams |
| **excalidraw** | `uv tool run excalidraw-mcp` | — | Create Excalidraw diagrams |
| **tyrell.wellick** | mcp-slack-extended server.py | SLACK_BOT_TOKEN, SLACK_TEAM_ID | Slack tools for Tyrell |
| **elliot.alderson** | mcp-slack-extended server.py | SLACK_BOT_TOKEN, SLACK_TEAM_ID | Slack tools for Elliot |
| **mr.robot** | mcp-slack-extended server.py | SLACK_BOT_TOKEN, SLACK_TEAM_ID | Slack tools for Mr. Robot |

## Project: bike-shop (agent runtime)

Config: `~/software_development/workoutspace/bike_shop/mcp.json`

| Server | Command | Env Vars | Purpose |
|--------|---------|----------|---------|
| **notion** | `uv tool run mcp-notion` | ${NOTION_API_KEY} from .env | Notion integration |
| **trello** | `uv tool run mcp-trello` | ${TRELLO_API_KEY}, ${TRELLO_TOKEN} from .env | Trello integration |
| **drawio** | `uv tool run drawio-mcp` | — | Architecture diagrams |
| **excalidraw** | `uv tool run excalidraw-mcp` | — | Whiteboard diagrams |

Note: bike-shop mcp.json uses `${VAR}` placeholders resolved from .env at runtime via `_resolve_env_vars()` in handlers.py.
