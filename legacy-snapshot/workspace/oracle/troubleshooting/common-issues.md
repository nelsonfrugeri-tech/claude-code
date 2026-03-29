# Troubleshooting — Problemas Comuns

## bike-shop

### Agents não respondem / timeout

**Sintoma**: Bot fica mudo após @mention ou DM.

**Diagnóstico**:
```bash
# Verificar se processo está rodando
ps aux | grep bike-shop

# Ver logs
# (bike-shop roda em foreground, logs vão para stdout)
```

**Causas comuns**:
1. **Token inválido**: Reinstalar Slack App e atualizar .env
2. **Socket Mode desconectou**: Reiniciar o processo
3. **Claude CLI travou**: subprocess sem timeout pode travar se Claude não responder — matar e reiniciar

### Edições no projeto errado

**Contexto**: O projeto bike-shop é instalado via `uv tool install -e .`, que cria um `.pth` file em:
```
~/.local/share/uv/tools/bike-shop/lib/python3.12/site-packages/_bike_shop.pth
```
Apontando para `/Users/nelson.frugeri/software_development/workoutspace/bike_shop/src`.

**Lição**: Sempre verificar o path real do projeto antes de editar. Existe também um `slack-agents` em `~/software_development/workoutspace/slack-agents/` que é um projeto DIFERENTE.

### PEM permission denied

```bash
chmod 600 ~/.ssh/bike-shop-*.pem
```

### GitHub push 403

**Causa**: Token do `gh` CLI não tem scope de admin.
**Solução**: `gh auth refresh --scopes repo,admin:org` ou fazer via GitHub UI.

### MCP env vars não resolvidas

**Causa**: `.env` não tem a variável que `mcp.json` referencia com `${VAR}`.
**Solução**: Verificar `.env` e garantir que todas as vars de `mcp.json` estão definidas.

## Claude Code

### Agent não encontrado

```
Error: Agent "nome" not found
```

**Solução**: Verificar que `~/.claude/agents/{nome}.md` existe e tem frontmatter válido.

### Skill não carrega

**Causa**: Path da skill incorreto ou arquivo `index.md` faltando.
**Solução**: Verificar `~/.claude/skills/{nome}/index.md` existe.

### memory-keeper não conecta

**Causa**: Script `~/.claude/hooks/run-memory-keeper.sh` não executável ou dependências faltando.
**Solução**:
```bash
chmod +x ~/.claude/hooks/run-memory-keeper.sh
# Verificar que o servidor MCP está rodando
```
