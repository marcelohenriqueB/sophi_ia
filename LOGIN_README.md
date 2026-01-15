# Página de Login - Sophi IA

## 📋 O que foi criado

Foi criada uma página de login completa no estilo do projeto, integrada com Inertia.js e Django.

### Arquivos criados/modificados:

#### 1. Frontend (Vue.js + Inertia)
- ✅ **`web/src/Pages/Auth/Login.vue`** - Página de login com design moderno
  - Gradiente de fundo matching o tema do projeto
  - Campos de email e senha com validação
  - Opção "Lembrar-me"
  - Botão "Esqueceu a senha?"
  - Mensagens de erro do backend
  - Toggle para mostrar/ocultar senha
  - Layout responsivo

#### 2. Backend (Django)
- ✅ **`users/views.py`** - Views de autenticação
  - `login_view` - Renderiza e processa login
  - `logout_view` - Processa logout
  - `home_view` - Redireciona para dashboard
  - `profile_view` - Visualizar perfil do usuário

- ✅ **`core/middleware.py`** - Middleware de autenticação
  - `redirect_if_not_authenticated` - Redireciona usuários não autenticados

- ✅ **`core/urls.py`** - Rotas de autenticação
  - `/` - Home (redireciona para reservas)
  - `/login` - Página de login
  - `/logout` - Logout
  - `/profile` - Perfil do usuário

- ✅ **`core/settings.py`** - Configurações
  - Middleware de redirecionamento adicionado
  - URLs de autenticação configuradas

#### 3. Layout atualizado
- ✅ **`web/src/Pages/Layouts/Layout.vue`** - Botão de logout funcional

## 🚀 Como usar

### 1. Criar um usuário de teste (se ainda não tiver)

```bash
cd c:\Users\marce\Desktop\sophi_ia
python manage.py createsuperuser
```

Ou via shell do Django:
```bash
python manage.py shell
```

```python
from users.models import User
user = User.objects.create_user(
    email='admin@sophiia.com',
    password='senha123',
    name='Administrador'
)
user.save()
```

### 2. Iniciar o servidor

Terminal 1 (Django):
```bash
python manage.py runserver
```

Terminal 2 (Vite - Frontend):
```bash
cd web
npm run dev
```

### 3. Acessar o sistema

1. Abra o navegador em `http://127.0.0.1:8000`
2. Você será automaticamente redirecionado para `/login`
3. Faça login com as credenciais criadas
4. Após o login, será redirecionado para `/viagens/reservas/list`

## 🎨 Características do Design

### Cores e Estilo
- **Gradiente de fundo**: Slate-700 → Slate-600 → Purple-600
- **Card branco** com sombra elevada
- **Bordas arredondadas** (rounded-2xl) - padrão do projeto
- **Ícones FontAwesome** - consistente com todo o projeto
- **DaisyUI** - componentes de input e button

### Componentes
- ✅ Logo do Sophi IA com ícone de navio
- ✅ Campos de input estilizados com ícones
- ✅ Toggle de visibilidade de senha
- ✅ Checkbox "Lembrar-me"
- ✅ Link "Esqueceu a senha?" (placeholder)
- ✅ Link "Cadastre-se" (placeholder)
- ✅ Mensagens de erro contextuais
- ✅ Loading state no botão
- ✅ Copyright no rodapé

## 🔒 Segurança

### Implementado:
- ✅ CSRF Protection via Django
- ✅ Autenticação por email (EmailBackend)
- ✅ Senhas hasheadas (Django password validators)
- ✅ Middleware de redirecionamento para rotas protegidas
- ✅ Session management (lembrar-me)
- ✅ Logout seguro

### Rotas públicas (sem autenticação):
- `/login`
- `/logout`
- `/admin/`
- `/static/*`
- `/assets/*`

### Rotas protegidas:
- Todas as outras rotas requerem autenticação
- Usuários não autenticados são redirecionados para `/login`

## 📝 Próximos passos (opcionais)

1. **Recuperação de senha**
   - Criar view para solicitar reset
   - Enviar email com token
   - Página de redefinição de senha

2. **Registro de usuários**
   - Criar página de cadastro
   - Validação de dados
   - Email de confirmação

3. **Two-Factor Authentication (2FA)**
   - Integrar TOTP
   - SMS verification

4. **Página de perfil**
   - Criar `Auth/Profile.vue`
   - Editar informações do usuário
   - Alterar senha

5. **Rate limiting**
   - Limitar tentativas de login
   - Prevenir brute force

## 🐛 Troubleshooting

### Problema: "Página de login não carrega"
- Verifique se o Vite está rodando (`npm run dev`)
- Verifique se o Django está rodando (`python manage.py runserver`)
- Limpe o cache do navegador

### Problema: "Erro 500 ao fazer login"
- Verifique se o usuário existe no banco
- Verifique os logs do Django no terminal
- Certifique-se de que as migrations foram aplicadas

### Problema: "Redirecionamento em loop"
- Verifique o middleware `redirect_if_not_authenticated`
- Certifique-se de que as rotas públicas estão corretas
- Limpe as sessions: `python manage.py clearsessions`

### Problema: "CSRF token missing"
- Verifique se `@ensure_csrf_cookie` está na view
- Verifique se o axios está configurado com CSRF headers
- Certifique-se de que o middleware CSRF está ativo

## 💡 Dicas

- O campo de email aceita login com o email cadastrado
- A senha é case-sensitive
- "Lembrar-me" mantém a sessão mesmo após fechar o navegador
- O botão de logout está na sidebar (canto inferior esquerdo)

## 🎯 Estrutura de Autenticação

```
Login Flow:
1. Usuário acessa qualquer rota protegida
2. Middleware verifica autenticação
3. Se não autenticado → Redireciona para /login
4. Usuário preenche credenciais
5. POST para /login
6. Django autentica (EmailBackend)
7. Se válido → Cria sessão → Redireciona para /
8. / redireciona para /viagens/reservas/list

Logout Flow:
1. Usuário clica em "Logout" na sidebar
2. POST para /logout (via Inertia router)
3. Django destroi sessão
4. Redireciona para /login
```

---

**Desenvolvido com ❤️ seguindo o padrão visual do Sophi IA**
