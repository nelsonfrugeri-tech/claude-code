# Adapter: Slack

## Como funciona

Os agents se comunicam via Slack usando Socket Mode (push-based, zero polling).

Quando alguém faz `@mention` de um agent num canal ou envia DM, o evento chega via WebSocket e o agent responde automaticamente.

## Gerenciamento

```bash
# Subir um agent
cd ~/software_development/workoutspace/slack-agents && uv run slack-agent <name>

# Em background
cd ~/software_development/workoutspace/slack-agents && nohup uv run slack-agent <name> > /tmp/slack-agent-<name>.log 2>&1 &

# Status
cd ~/software_development/workoutspace/slack-agents && uv run slack-agent --status

# Parar (gracioso)
cd ~/software_development/workoutspace/slack-agents && uv run slack-agent --stop <name>
```

## Nomes dos agents

| Agent           | CLI name   |
|-----------------|------------|
| Mr. Robot       | mr-robot   |
| Elliot Alderson | elliot     |
| Tyrell Wellick  | tyrell     |

## Logs

- `/tmp/slack-agent-mr-robot.log`
- `/tmp/slack-agent-elliot.log`
- `/tmp/slack-agent-tyrell.log`

## Regras

- **NUNCA** use `kill -9` — sempre `--stop` para shutdown gracioso
- Um agent por instância — o PID file previne duplicatas
- Logs em nível INFO mostram mensagens recebidas/respondidas
