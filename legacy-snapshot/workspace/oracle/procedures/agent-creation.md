# Agent Creation — Procedimento

## Quando usar
Quando precisar criar um novo agent no ecossistema Claude Code.

## Pré-requisitos
- Entender o papel/persona do agent
- Definir quais tools e skills precisa

## Passo a passo

### 1. Criar o arquivo do agent

```bash
touch ~/.claude/agents/{nome-do-agent}.md
```

### 2. Definir o frontmatter

```yaml
---
name: nome-do-agent
description: >
  Descrição concisa do que o agent faz.
  DEVE SER USADO para: {casos de uso específicos}.
tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch
model: opus
skills: arch-py, ai-engineer
---
```

**Campos obrigatórios:**
- `name`: identificador (usado com `claude --agent {name}`)
- `description`: o que faz + quando usar
- `tools`: lista de tools disponíveis
- `model`: `opus`, `sonnet`, ou `haiku`

**Campos opcionais:**
- `skills`: skills a carregar
- `color`: cor no terminal
- `permissionMode`: `default`, `bypassPermissions`, `plan`, etc.

### 3. Definir persona e workflow no body

Após o frontmatter (`---`), escreva:
- Identidade e personalidade
- Responsabilidades
- Workflow (o que fazer ao iniciar, durante, ao encerrar)
- Regras e princípios

### 4. Registrar no ecosystem

Atualize `~/.claude/workspace/oracle/ecosystem/agents.md` com o novo agent.

### 5. Se agent Slack: criar Slack App

Siga `procedures/slack-app-setup.md`.

### 6. Se agent precisa de GitHub: criar GitHub App

Siga `procedures/github-app-setup.md`.

### 7. Testar

```bash
claude --agent {nome-do-agent}
```

## Tools disponíveis

| Tool | Descrição |
|------|-----------|
| Read | Ler arquivos |
| Write | Criar/sobrescrever arquivos |
| Edit | Editar arquivos (find & replace) |
| Grep | Buscar conteúdo em arquivos |
| Glob | Buscar arquivos por padrão |
| Bash | Executar comandos shell |
| WebSearch | Buscar na web |
| WebFetch | Fetch de URLs |
| Task | Spawnar sub-agents |
| AskUserQuestion | Perguntar ao usuário |

## Modelos disponíveis

| Model | Uso |
|-------|-----|
| opus | Tarefas complexas, arquitetura, decisões críticas |
| sonnet | Tarefas médias, desenvolvimento geral |
| haiku | Tarefas simples, rápidas, baixo custo |
