# Oracle Knowledge Base — Index

Last updated: 2026-03-26

## Ecosystem Overview

- **Agents**: 13 agents em `~/.claude/agents/` → ver `ecosystem/agents.md`
- **Skills**: 4 skills em `~/.claude/skills/` → ver `ecosystem/skills.md`
- **MCP Servers**: memory-keeper (global) + per-project configs → ver `ecosystem/mcp-servers.md`
- **Workspaces**: 3 projetos ativos → ver `ecosystem/` e `projects/`

## Active Projects

| Project | Path | Status |
|---------|------|--------|
| bike-shop | `~/software_development/workoutspace/bike_shop/` | Active — multi-agent Slack team |
| lm-gateway | `~/software_development/workoutspace/artificial_intelligence/lm_gateway/` | Active |

## Recent Changes (2026-03-26)

- Created Oracle agent (`~/.claude/agents/oracle.md`)
- bike-shop: implemented memory system (session tracking + MEMORY.md)
- bike-shop: async processing, no timeout, resilience instructions
- bike-shop: team mentions (agents @mention each other)
- bike-shop: security audit — secrets moved to .env, PEMs to ~/.ssh/
- bike-shop: added draw.io + Excalidraw MCPs
- bike-shop: pushed to GitHub (nelsonfrugeri-tech/bike-shop), branch feat/improvement created

## Knowledge Base Status

All files populated:
- `ecosystem/` — agents.md, skills.md, mcp-servers.md ✓
- `procedures/` — slack-app-setup.md, github-app-setup.md, agent-creation.md, mcp-setup.md ✓
- `projects/` — bike-shop.md ✓
- `troubleshooting/` — common-issues.md ✓

## Pending

- Document lm-gateway project (`projects/lm-gateway.md`)
- Document ecosystem settings (`ecosystem/settings.md`)
- Update GitHub repo description (needs `gh auth refresh --scopes admin:org`)
