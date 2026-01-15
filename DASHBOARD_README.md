# Dashboard de Reservas

## 📊 Funcionalidades Implementadas

Foi criado um dashboard completo para a página inicial do sistema com as seguintes funcionalidades:

### 1. **Total de Reservas Hoje**
- Exibe o número de reservas feitas na data atual
- Card com ícone de calendário em azul

### 2. **Reservas dos Últimos 7 Dias**
- Total de reservas dos últimos 7 dias
- Gráfico de linha mostrando a evolução diária
- Card com ícone de semana em verde

### 3. **Vendas dos Últimos 30 Dias**
- Total de vendas (em R$) dos últimos 30 dias
- Gráfico de barras mostrando o valor de vendas por dia
- Card com ícone de dólar em roxo
- Valores formatados em reais (R$)

## 🛠️ Arquivos Criados/Modificados

### Backend (Django)

1. **`viagens/views.py`**
   - Criada a classe `DashboardView` que retorna os dados estatísticos
   - Endpoint GET que retorna JSON com:
     - `reservas_hoje`: número de reservas do dia
     - `total_reservas_7_dias`: total dos últimos 7 dias
     - `reservas_7_dias`: array com contagem diária
     - `vendas_30_dias`: array com valores diários
     - `total_vendas_30_dias`: soma total de vendas

2. **`viagens/urls.py`**
   - Adicionada rota: `path('dashboard', DashboardView.as_view(), name='dashboard')`
   - URL completa: `/viagens/dashboard`

3. **`users/views.py`**
   - Criada função `dashboard_view` para renderizar a página inicial
   - Usa Inertia.js para renderizar o componente Vue

4. **`core/urls.py`**
   - Adicionada rota raiz `path('', user_views.dashboard_view, name='home')`
   - Dashboard agora é a página inicial do sistema

### Frontend (Vue.js)

1. **`web/src/Pages/Dashboard/Index.vue`**
   - Componente Vue completo com:
     - 3 cards de estatísticas com ícones Font Awesome
     - 2 gráficos usando Chart.js:
       - Gráfico de linha para reservas dos últimos 7 dias
       - Gráfico de barras para vendas dos últimos 30 dias
     - Botão de atualização com animação de loading
     - Modal de carregamento durante requisições
     - Formatação de valores em reais
     - Formatação de datas em pt-BR
     - Design responsivo com Tailwind CSS

2. **`package.json`**
   - Adicionada dependência: `chart.js` para criação de gráficos

## 🚀 Como Usar

1. **Instale as dependências do frontend** (se ainda não instalou):
   ```bash
   cd web
   npm install
   ```

2. **Inicie o servidor Django**:
   ```bash
   python manage.py runserver
   ```

3. **Inicie o servidor de desenvolvimento do frontend**:
   ```bash
   cd web
   npm run dev
   ```

4. **Acesse o sistema**:
   - Faça login em: `http://localhost:8000/login`
   - Você será redirecionado automaticamente para o dashboard: `http://localhost:8000/`

## 📈 API do Dashboard

### Endpoint
```
GET /viagens/dashboard
```

### Resposta (JSON)
```json
{
  "reservas_hoje": 5,
  "total_reservas_7_dias": 23,
  "reservas_7_dias": [
    {"data": "2026-01-08", "total": 3},
    {"data": "2026-01-09", "total": 4},
    ...
  ],
  "vendas_30_dias": [
    {"data": "2025-12-15", "valor": 1500.00},
    {"data": "2025-12-16", "valor": 2300.50},
    ...
  ],
  "total_vendas_30_dias": 45000.75
}
```

### Autenticação
- Requer usuário autenticado
- Dados filtrados por `client` do usuário logado

## 🎨 Design

- **Cards de Estatísticas**: Design moderno com bordas coloridas à esquerda
- **Gráficos**: Interativos e responsivos usando Chart.js
- **Cores**: 
  - Azul: Reservas hoje
  - Verde: Reservas 7 dias
  - Roxo: Vendas 30 dias
- **Layout**: Grid responsivo que se adapta a diferentes tamanhos de tela

## 🔄 Atualização de Dados

- Dados são carregados automaticamente ao abrir a página
- Botão "Atualizar" permite recarregar os dados manualmente
- Animação de loading durante o carregamento

## ⚠️ Observações

- Os dados são filtrados pelo `client` do usuário logado
- Apenas reservas associadas ao cliente do usuário são exibidas
- As datas são formatadas no padrão brasileiro (DD/MM)
- Os valores monetários são formatados em reais (R$)
