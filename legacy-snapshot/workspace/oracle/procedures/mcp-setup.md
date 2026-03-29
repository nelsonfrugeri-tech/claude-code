# MCP Server Setup — Procedimento

## Quando usar
Quando precisar adicionar um novo MCP server ao ecossistema.

## Conceito

MCP (Model Context Protocol) servers fornecem tools extras ao Claude Code. Existem 2 níveis de config:

1. **Global** (`~/.claude.json` → `mcpServers`): disponível em todas as sessões
2. **Per-project** (`{project}/mcp.json` ou `~/.claude.json` → `projects.{path}.mcpServers`): disponível apenas naquele projeto

## Passo a passo

### 1. Instalar o MCP server

Maioria usa `uv tool`:
```bash
uv tool install {package-name}
# ou para rodar sem instalar:
uv tool run {package-name}
```

### 2. Configurar — Global

Edite `~/.claude.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "uv",
      "args": ["tool", "run", "package-name"],
      "env": {
        "API_KEY": "valor"
      }
    }
  }
}
```

### 3. Configurar — Per-project

Crie `mcp.json` na raiz do projeto:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "uv",
      "args": ["tool", "run", "package-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Nota**: Use `${VAR}` para secrets — o bike-shop resolve esses placeholders do `.env` em runtime via `_resolve_env_vars()` em `handlers.py`.

### 4. Configurar — Via ~/.claude.json per-project

```json
{
  "projects": {
    "/path/to/project": {
      "mcpServers": {
        "server-name": { ... }
      }
    }
  }
}
```

## MCP Servers conhecidos

| Server | Package | Purpose |
|--------|---------|---------|
| memory-keeper | custom script | Persistent memory |
| arxiv-mcp-server | `arxiv-mcp-server` | arXiv papers |
| trello | `mcp-trello` | Trello boards |
| notion | `mcp-notion` | Notion pages/DBs |
| drawio | `drawio-mcp` | Draw.io diagrams |
| excalidraw | `excalidraw-mcp` | Excalidraw diagrams |
| mcp-slack-extended | custom `server.py` | Slack tools (custom) |

## Verificação

1. Reinicie o Claude Code
2. O server aparece na lista de tools disponíveis
3. Tools do server funcionam (teste com uma operação simples)

## Troubleshooting

- **Server não aparece**: Verificar JSON syntax em `~/.claude.json` ou `mcp.json`
- **"command not found"**: `uv tool install` o package primeiro
- **Env vars não resolvidas**: Para `${VAR}` placeholders, garantir que `.env` tem a variável
