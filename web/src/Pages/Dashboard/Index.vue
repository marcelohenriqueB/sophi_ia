<template>
  
    <div class="p-6 space-y-6">
      <!-- Cabeçalho -->
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button 
          @click="carregarDados" 
          class="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-800 transition-colors"
        >
          <font-awesome-icon icon="sync" :class="{ 'animate-spin': loading }" /> 
          Atualizar
        </button>
      </div>

      <!-- Cards de Estatísticas -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Card: Reservas Hoje -->
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Reservas Hoje</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ dadosDashboard.reservas_hoje || 0 }}</p>
            </div>
            <div class="bg-blue-100 p-3 rounded-full">
              <font-awesome-icon icon="calendar-day" class="text-blue-500 text-2xl" />
            </div>
          </div>
        </div>

        <!-- Card: Total Últimos 7 Dias -->
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Últimos 7 Dias</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ dadosDashboard.total_reservas_7_dias || 0 }}</p>
            </div>
            <div class="bg-green-100 p-3 rounded-full">
              <font-awesome-icon icon="calendar-week" class="text-green-500 text-2xl" />
            </div>
          </div>
        </div>

        <!-- Card: Vendas 30 Dias -->
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Vendas (30 dias)</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">
                {{ formatarMoeda(dadosDashboard.total_vendas_30_dias || 0) }}
              </p>
            </div>
            <div class="bg-purple-100 p-3 rounded-full">
              <font-awesome-icon icon="dollar-sign" class="text-purple-500 text-2xl" />
            </div>
          </div>
        </div>

        <!-- Card: Suítes Reservadas Hoje -->
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-orange-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Suítes Reservadas Hoje</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ dadosDashboard.suites_reservadas_hoje || 0 }}</p>
            </div>
            <div class="bg-orange-100 p-3 rounded-full">
              <font-awesome-icon icon="door-open" class="text-orange-500 text-2xl" />
            </div>
          </div>
        </div>

        <!-- Card: Total de Passageiros Hoje -->
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-cyan-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Passageiros Hoje</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ dadosDashboard.total_passageiros_hoje || 0 }}</p>
            </div>
            <div class="bg-cyan-100 p-3 rounded-full">
              <font-awesome-icon icon="users" class="text-cyan-500 text-2xl" />
            </div>
          </div>
        </div>

        <!-- Card: Rota Mais Usada -->
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-rose-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Rota Mais Usada Hoje</p>
              <p class="text-xl font-bold text-gray-900 mt-2">{{ dadosDashboard.rota_mais_usada?.nome || 'Nenhuma' }}</p>
              <p class="text-sm text-gray-500 mt-1">{{ dadosDashboard.rota_mais_usada?.total || 0 }} reservas</p>
            </div>
            <div class="bg-rose-100 p-3 rounded-full">
              <font-awesome-icon icon="route" class="text-rose-500 text-2xl" />
            </div>
          </div>
        </div>
      </div>

      <!-- Gráficos -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Gráfico: Reservas dos Últimos 7 Dias -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4">
            <font-awesome-icon icon="chart-line" class="mr-2 text-green-600" />
            Reservas - Últimos 7 Dias
          </h2>
          <canvas ref="chartReservas7Dias" class="w-full" style="max-height: 300px;"></canvas>
        </div>

        <!-- Gráfico: Vendas dos Últimos 30 Dias -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4">
            <font-awesome-icon icon="chart-bar" class="mr-2 text-purple-600" />
            Vendas - Últimos 30 Dias
          </h2>
          <canvas ref="chartVendas30Dias" class="w-full" style="max-height: 300px;"></canvas>
        </div>
      </div>

      <!-- Mensagem de Carregamento -->
      <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-8 flex flex-col items-center">
          <font-awesome-icon icon="spinner" class="text-4xl text-slate-700 animate-spin mb-4" />
          <p class="text-gray-700 font-medium">Carregando dados...</p>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

interface ReservaData {
  data: string;
  total: number;
}

interface VendaData {
  data: string;
  valor: number;
}

interface RotaMaisUsada {
  nome: string;
  total: number;
}

interface DadosDashboard {
  reservas_hoje: number;
  total_reservas_7_dias: number;
  reservas_7_dias: ReservaData[];
  vendas_30_dias: VendaData[];
  total_vendas_30_dias: number;
  suites_reservadas_hoje: number;
  total_passageiros_hoje: number;
  rota_mais_usada: RotaMaisUsada;
}

const loading = ref(false);
const dadosDashboard = ref<DadosDashboard>({
  reservas_hoje: 0,
  total_reservas_7_dias: 0,
  reservas_7_dias: [],
  vendas_30_dias: [],
  total_vendas_30_dias: 0,
  suites_reservadas_hoje: 0,
  total_passageiros_hoje: 0,
  rota_mais_usada: { nome: 'Nenhuma', total: 0 }
});

const chartReservas7Dias = ref<HTMLCanvasElement | null>(null);
const chartVendas30Dias = ref<HTMLCanvasElement | null>(null);

let chartReservasInstance: Chart | null = null;
let chartVendasInstance: Chart | null = null;

const formatarMoeda = (valor: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor);
};

const formatarData = (dataStr: string): string => {
  const data = new Date(dataStr + 'T00:00:00');
  return data.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
};

const carregarDados = async () => {
  loading.value = true;
  try {
    const response = await fetch('/viagens/dashboard', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar dados do dashboard');
    }

    const dados = await response.json();
    dadosDashboard.value = dados;

    await nextTick();
    criarGraficos();
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    alert('Erro ao carregar dados do dashboard. Tente novamente.');
  } finally {
    loading.value = false;
  }
};

const criarGraficos = () => {
  // Gráfico de Reservas dos Últimos 7 Dias
  if (chartReservas7Dias.value) {
    if (chartReservasInstance) {
      chartReservasInstance.destroy();
    }

    const labels = dadosDashboard.value.reservas_7_dias.map(item => formatarData(item.data));
    const data = dadosDashboard.value.reservas_7_dias.map(item => item.total);

    chartReservasInstance = new Chart(chartReservas7Dias.value, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Reservas',
          data: data,
          borderColor: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: 'rgb(34, 197, 94)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      }
    });
  }

  // Gráfico de Vendas dos Últimos 30 Dias
  if (chartVendas30Dias.value) {
    if (chartVendasInstance) {
      chartVendasInstance.destroy();
    }

    const labels = dadosDashboard.value.vendas_30_dias.map(item => formatarData(item.data));
    const data = dadosDashboard.value.vendas_30_dias.map(item => item.valor);

    chartVendasInstance = new Chart(chartVendas30Dias.value, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Vendas (R$)',
          data: data,
          backgroundColor: 'rgba(168, 85, 247, 0.7)',
          borderColor: 'rgb(168, 85, 247)',
          borderWidth: 1,
          borderRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.parsed.y ?? 0;
                return formatarMoeda(value);
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return 'R$ ' + value.toLocaleString('pt-BR');
              }
            }
          }
        }
      }
    });
  }
};

onMounted(() => {
  carregarDados();
});
</script>

<style scoped>
.active {
  background-color: #475569;
}
</style>
