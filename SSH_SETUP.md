# Teste local de conexão SSH

## 1. Verificar se a chave SSH está correta
```bash
# Testar se a chave privada é válida
ssh-keygen -y -f ~/.ssh/id_rsa

# Se der erro, a chave está corrompida ou em formato inválido
```

## 2. Testar conexão SSH manualmente
```bash
# Conectar ao servidor
ssh -i ~/.ssh/id_rsa seu-usuario@seu-host

# Se pedir senha, a chave não está em authorized_keys
# Se disser "Permission denied (publickey)", a chave pública não está lá
```

## 3. Setup correto da chave no servidor
No **servidor** (execute estas linhas):

```bash
# 1. Se não tem .ssh, criar
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 2. Se tem chave privada em outro lugar, extrair a pública
ssh-keygen -y -f /caminho/para/chave/privada > ~/.ssh/id_rsa.pub

# 3. Adicionar a chave pública em authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 4. Testar localmente
ssh -i ~/.ssh/id_rsa localhost
# Deve conectar sem pedir senha
```

## 4. Gerar nova chave (se a atual não funciona)
No **servidor**:
```bash
# Gerar nova chave SSH
ssh-keygen -t ed25519 -f ~/.ssh/id_rsa -N ""

# Copiar a chave pública para authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Extrair a chave privada para usar no GitHub
cat ~/.ssh/id_rsa
# Copie todo o conteúdo (incluindo BEGIN e END) para GitHub Secrets SSH_KEY
```

## 5. No GitHub, adicionar o secret corretamente
- Settings → Secrets and variables → Actions
- New repository secret
- Name: `SSH_KEY`
- Value: Cole **todo** o conteúdo da chave privada (`-----BEGIN...-----END...`)

## 6. Permissões importantes no servidor
```bash
# Verifique permissões
ls -la ~/.ssh/
# Deve mostrar:
# -rw------- id_rsa
# -rw-r--r-- id_rsa.pub
# -rw------- authorized_keys

# Se estiver errado, corrigir
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/authorized_keys
```

## Troubleshooting

### "Permission denied (publickey)"
- Chave pública **não está** em `~/.ssh/authorized_keys` do servidor
- Solução: adicione com `cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`

### "Host key verification failed"
- Servidor não é conhecido
- Solução: o workflow já trata isso com `ssh-keyscan`

### "Could not parse key"
- Formato da chave errado (provavelmente truncada)
- Solução: copie **todo** o conteúdo incluindo `-----BEGIN OPENSSH PRIVATE KEY-----` e `-----END OPENSSH PRIVATE KEY-----`
