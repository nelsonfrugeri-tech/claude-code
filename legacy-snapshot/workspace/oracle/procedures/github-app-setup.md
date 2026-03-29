# GitHub App Setup — Procedimento Completo

## Quando usar
Quando precisar que um agent tenha identidade própria no GitHub (commits, PRs, issues com avatar e nome do agent).

## Pré-requisitos
- Conta GitHub com permissões para criar GitHub Apps
- Acesso a https://github.com/settings/apps

## Passo a passo

### 1. Criar o GitHub App

1. Acesse https://github.com/settings/apps → **New GitHub App**
2. Preencha:
   - **GitHub App name**: nome do agent (ex: "Elliot Alderson Bot")
   - **Homepage URL**: URL do repo ou qualquer URL válida
   - **Webhook**: desmarque "Active" (não precisamos de webhooks)

### 2. Configurar Permissões

Em **Permissions**:

**Repository permissions:**
- Contents: Read & Write (commits, push)
- Issues: Read & Write (criar/comentar issues)
- Pull requests: Read & Write (criar/comentar PRs)
- Metadata: Read-only (obrigatório)

**Organization permissions:** (se aplicável)
- Members: Read-only

### 3. Gerar Private Key

1. Após criar o app, vá para **General** → **Private keys**
2. Click **Generate a private key**
3. Será feito download de um `.pem`
4. Mova para local seguro:
```bash
mv ~/Downloads/*.pem ~/.ssh/bike-shop-{agent-name}.pem
chmod 600 ~/.ssh/bike-shop-{agent-name}.pem
```

### 4. Instalar o App no Repositório

1. Vá para **Install App** no menu lateral
2. Selecione sua conta/organização
3. Escolha **Only select repositories** → selecione o repo alvo
4. Click **Install**

### 5. Coletar IDs

Após criar o app:

| Dado | Onde encontrar |
|------|----------------|
| **App ID** | General → About → App ID |
| **Installation ID** | URL após instalar: `https://github.com/settings/installations/{ID}` |
| **Private Key** | Arquivo .pem baixado |

### 6. Configurar no .env

```env
# GitHub App — Elliot Alderson
ELLIOT_GITHUB_APP_ID=123456
ELLIOT_GITHUB_INSTALLATION_ID=78901234
ELLIOT_GITHUB_PEM_PATH=~/.ssh/bike-shop-elliot-alderson.pem
```

### 7. Como funciona a autenticação

O código gera um JWT token a partir do App ID + PEM, depois troca por um Installation Token:

```python
import jwt, time, requests

# 1. Gerar JWT
now = int(time.time())
payload = {"iat": now - 60, "exp": now + 600, "iss": APP_ID}
token = jwt.encode(payload, pem_content, algorithm="RS256")

# 2. Trocar por Installation Token
resp = requests.post(
    f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens",
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
)
install_token = resp.json()["token"]

# 3. Usar em git
# git -c "http.extraHeader=Authorization: token {install_token}" push
```

## Verificação

1. O app aparece em https://github.com/settings/apps
2. Está instalado no repositório alvo
3. JWT generation funciona (sem erros de PEM)
4. Consegue fazer push com o installation token

## Troubleshooting

- **"Could not verify JWT"**: PEM corrompido ou App ID errado
- **403 on push**: Installation ID errado ou app não instalado no repo
- **PEM permission denied**: `chmod 600 ~/.ssh/*.pem`
- **JWT expired**: Clock skew — JWT tem validade de 10min, verificar horário do sistema
