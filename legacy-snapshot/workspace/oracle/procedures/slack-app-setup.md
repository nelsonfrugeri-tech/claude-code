# Slack App Setup — Procedimento Completo

## Quando usar
Quando precisar criar um novo bot/agent Slack para o ecossistema bike-shop (ou similar).

## Pré-requisitos
- Conta Slack com permissões de admin no workspace
- Acesso a https://api.slack.com/apps

## Passo a passo

### 1. Criar o Slack App

1. Acesse https://api.slack.com/apps → **Create New App**
2. Escolha **From scratch**
3. Nome: nome do agent (ex: "Elliot Alderson", "Mr. Robot", "Tyrell Wellick")
4. Workspace: selecione o workspace alvo

### 2. Configurar Bot Token Scopes

Em **OAuth & Permissions** → **Bot Token Scopes**, adicione:

```
app_mentions:read    — Receber @mentions
channels:history     — Ler mensagens de canais públicos
channels:read        — Listar canais públicos
chat:write           — Enviar mensagens
groups:history       — Ler mensagens de canais privados
groups:read          — Listar canais privados
im:history           — Ler DMs
im:read              — Listar DMs
im:write             — Enviar DMs
mpim:history         — Ler group DMs
mpim:read            — Listar group DMs
reactions:read       — Ler reactions
reactions:write      — Adicionar reactions
users:read           — Ler info de usuários
```

### 3. Configurar Event Subscriptions

Em **Event Subscriptions**:
1. Toggle **Enable Events** → On
2. **Request URL**: não necessário para Socket Mode
3. **Subscribe to bot events**:
   - `app_mention` — quando alguém @menciona o bot
   - `message.channels` — mensagens em canais públicos
   - `message.groups` — mensagens em canais privados
   - `message.im` — DMs diretas
   - `message.mpim` — group DMs

### 4. Habilitar Socket Mode

Em **Socket Mode**:
1. Toggle **Enable Socket Mode** → On
2. Gerar um **App-Level Token** com scope `connections:write`
3. Nome sugerido: `socket-token`
4. Salvar o token (`xapp-...`)

### 5. Instalar no Workspace

Em **Install App**:
1. Click **Install to Workspace**
2. Autorize as permissões
3. Copie o **Bot User OAuth Token** (`xoxb-...`)

### 6. Coletar Tokens

Você precisa de 2 tokens por bot:

| Token | Formato | Onde encontrar |
|-------|---------|----------------|
| **Bot Token** | `xoxb-...` | OAuth & Permissions → Bot User OAuth Token |
| **App Token** | `xapp-...` | Basic Information → App-Level Tokens |

### 7. Configurar no .env do projeto

```env
# Agent: Elliot Alderson
ELLIOT_SLACK_BOT_TOKEN=xoxb-...
ELLIOT_SLACK_APP_TOKEN=xapp-...

# Agent: Mr. Robot
MR_ROBOT_SLACK_BOT_TOKEN=xoxb-...
MR_ROBOT_SLACK_APP_TOKEN=xapp-...

# Agent: Tyrell Wellick
TYRELL_SLACK_BOT_TOKEN=xoxb-...
TYRELL_SLACK_APP_TOKEN=xapp-...
```

### 8. Obter Bot User ID e Team ID

Após instalar, execute:
```bash
curl -s -H "Authorization: Bearer xoxb-YOUR-TOKEN" https://slack.com/api/auth.test | python3 -m json.tool
```

Retorna:
```json
{
  "user_id": "U0AP10P0GNM",   ← Bot User ID (para @mentions)
  "team_id": "T08N5UWJBUE"    ← Team/Workspace ID
}
```

Adicione ao .env:
```env
ELLIOT_SLACK_TEAM_ID=T08N5UWJBUE
```

## Verificação

1. O bot aparece no workspace Slack
2. Pode ser @mencionado em canais
3. Responde a DMs
4. `auth.test` retorna dados válidos

## Troubleshooting

- **Bot não responde a @mentions**: Verificar Event Subscriptions → `app_mention` está subscrito
- **Bot não recebe DMs**: Verificar `im:history` e `message.im` estão habilitados
- **"not_authed" error**: Token expirado ou inválido, reinstalar o app
- **Socket mode não conecta**: Verificar App-Level Token tem scope `connections:write`
