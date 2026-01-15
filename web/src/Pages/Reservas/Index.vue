<template>
    <div class="border border-gray-200 rounded-2xl py-6 bg-white">
        <div class="px-6 flex justify-between items-center mb-4">
            <div class="flex justify-between">
                <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                    <font-awesome-icon icon="calendar-check" class="text-white" />
                </span>
                <div class="flex flex-col justify-center">
                    <h2 class="text-lg font-medium">Reservas</h2>
                    <p class="text-sm font-normal text-slate-600 my-0">
                        Visualize todas as reservas cadastradas na plataforma.
                    </p>
                </div>
            </div>

            <a href="/viagens/reservas/create" class="btn btn-primary rounded-2xl">
                <font-awesome-icon icon="plus" class="mr-2" />
                Nova Reserva
            </a>
        </div>

        <hr class="my-4 border-gray-200" />

        <div class="px-6 grid grid-cols-1 lg:grid-cols-4 gap-6 mt-6">
            <!-- Calendário -->
            <div class="lg:col-span-1">
                <div class="bg-white rounded-xl shadow-md p-4 sticky top-4">
                    <div class="flex justify-between items-center mb-4">
                        <button @click="mesAnterior" class="btn btn-sm btn-circle">
                            <font-awesome-icon icon="chevron-left" />
                        </button>
                        <h3 class="text-lg font-bold">{{ mesAtualNome }}</h3>
                        <button @click="proximoMes" class="btn btn-sm btn-circle">
                            <font-awesome-icon icon="chevron-right" />
                        </button>
                    </div>

                    <!-- Dias da semana -->
                    <div class="grid grid-cols-7 gap-1 mb-2">
                        <div v-for="dia in diasSemana" :key="dia" class="text-center text-xs font-medium text-gray-600">
                            {{ dia }}
                        </div>
                    </div>

                    <!-- Dias do mês -->
                    <div class="grid grid-cols-7 gap-1">
                        <div v-for="(dia, index) in diasDoMes" :key="index" 
                            class="aspect-square flex items-center justify-center text-sm rounded-lg cursor-pointer transition-all"
                            :class="getDiaClasses(dia)"
                            @click="selecionarDia(dia)">
                            {{ dia?.dia || '' }}
                        </div>
                    </div>

                    <!-- Legenda -->
                    <div class="mt-4 space-y-2 text-xs">
                        <div class="flex items-center gap-2">
                            <div class="w-4 h-4 bg-blue-500 rounded"></div>
                            <span>Dia selecionado</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <div class="w-4 h-4 bg-green-100 border-2 border-green-500 rounded"></div>
                            <span>Com reservas</span>
                        </div>
                    </div>
                </div>

                <!-- Filtros -->
                <div class="bg-white rounded-xl shadow-md p-4 mt-4">
                    <h3 class="text-lg font-bold mb-4">Filtros</h3>
                    
                    <div class="space-y-3">
                        <div>
                            <label class="text-sm font-medium text-gray-700">Rota</label>
                            <select v-model="filtros.rota" @change="aplicarFiltros" 
                                class="select select-bordered w-full mt-1">
                                <option value="">Todas as rotas</option>
                                <option v-for="rota in rotas" :key="rota.id" :value="rota.id">
                                    {{ rota.nome }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-gray-700">Suíte</label>
                            <select v-model="filtros.suite" @change="aplicarFiltros" 
                                class="select select-bordered w-full mt-1">
                                <option value="">Todas as suítes</option>
                                <option v-for="suite in suites" :key="suite.id" :value="suite.id">
                                    {{ suite.nome }}
                                </option>
                            </select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-gray-700">Status</label>
                            <select v-model="filtros.status" @change="aplicarFiltros" 
                                class="select select-bordered w-full mt-1">
                                <option value="">Todos os status</option>
                                <option value="RESERVADA">Reservada</option>
                                <option value="CONFIRMADA">Confirmada</option>
                                <option value="UTILIZADA">Utilizada</option>
                                <option value="CANCELADA">Cancelada</option>
                                <option value="REEMBOLSADA">Reembolsada</option>
                            </select>
                        </div>

                        <button @click="limparFiltros" class="btn btn-outline w-full">
                            <font-awesome-icon icon="times" class="mr-2" />
                            Limpar Filtros
                        </button>
                    </div>
                </div>
            </div>

            <!-- Lista de Reservas -->
            <div class="lg:col-span-3">
                <div class="flex justify-between items-center mb-4">
                    <h1 class="text-2xl font-bold">Lista de Reservas</h1>
                    <span v-if="dataSelecionada" class="badge badge-lg badge-primary">
                        {{ formatarDataCompleta(dataSelecionada) }}
                    </span>
                </div>

                <div v-if="carregando" class="flex justify-center items-center h-64">
                    <font-awesome-icon icon="spinner" class="text-4xl animate-spin text-slate-600" />
                </div>

                <div v-else-if="reservasFiltradas.length === 0" class="text-center py-12">
                    <font-awesome-icon icon="inbox" class="text-6xl text-gray-300 mb-4" />
                    <p class="text-gray-500">Nenhuma reserva encontrada</p>
                </div>

                <div v-else class="overflow-x-auto">
                    <table class="table table-sm w-full">
                        <thead>
                            <tr class="bg-slate-200">
                                <th>ID</th>
                                <th>Cliente</th>
                                <th>Rota</th>
                                <th>Suíte</th>
                                <th>Valor</th>
                                <th>Pagamento</th>
                                <th>Status</th>
                                <th>Data</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="reserva in reservasFiltradas" :key="reserva.id" class="hover:bg-slate-100">
                                <td>{{ reserva.id }}</td>
                                <td>{{ reserva.customer.nome }}</td>
                                <td>{{ reserva.rota?.nome || '-' }}</td>
                                <td>{{ reserva.suite?.nome || '-' }}</td>
                                <td>R$ {{ formatCurrency(reserva.valor_total) }}</td>
                                <td>
                                    <span :class="reserva.pago ? 'badge badge-success' : 'badge badge-warning'">
                                        {{ reserva.pago ? 'Pago' : 'Pendente' }}
                                    </span>
                                </td>
                                <td>
                                    <span :class="getStatusBadgeClass(reserva.status_reserva)">
                                        {{ getStatusLabel(reserva.status_reserva) }}
                                    </span>
                                </td>
                                <td>{{ formatDate(reserva.data_reserva) }}</td>
                                <td class="flex gap-2">
                                    <Link :href="`/viagens/reservas/${reserva.id}/edit`" 
                                        class="btn btn-sm bg-green-500 text-white rounded-lg">
                                        <font-awesome-icon icon="eye" />
                                    </Link>
                                    <button @click="confirmDelete(reserva.id)"
                                        class="btn btn-sm bg-red-500 text-white rounded-lg">
                                        <font-awesome-icon icon="trash" />
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { router } from '@inertiajs/vue3'
import { Link } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

const props = defineProps({
    reservas: {
        type: Array,
        required: true
    },
    rotas: {
        type: Array,
        default: () => []
    },
    suites: {
        type: Array,
        default: () => []
    }
})

const diasSemana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

const mesAtual = ref(new Date())
const dataSelecionada = ref(null)
const carregando = ref(false)
const todasReservas = ref(props.reservas)
const rotas = ref(props.rotas)
const suites = ref(props.suites)

const filtros = ref({
    rota: '',
    suite: '',
    status: ''
})

const mesAtualNome = computed(() => {
    return mesAtual.value.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })
})

const diasDoMes = computed(() => {
    const ano = mesAtual.value.getFullYear()
    const mes = mesAtual.value.getMonth()
    
    const primeiroDia = new Date(ano, mes, 1)
    const ultimoDia = new Date(ano, mes + 1, 0)
    
    const dias = []
    
    for (let i = 0; i < primeiroDia.getDay(); i++) {
        dias.push(null)
    }
    
    for (let dia = 1; dia <= ultimoDia.getDate(); dia++) {
        const data = new Date(ano, mes, dia)
        dias.push({
            dia,
            data,
            temReservas: verificarSeTemReservas(data)
        })
    }
    
    return dias
})

function verificarSeTemReservas(data) {
    const dataStr = data.toISOString().split('T')[0]
    return todasReservas.value.some(reserva => {
        const reservaData = new Date(reserva.data_reserva).toISOString().split('T')[0]
        return reservaData === dataStr
    })
}

function getDiaClasses(dia) {
    if (!dia) return ''
    
    const dataStr = dia.data.toISOString().split('T')[0]
    const hoje = new Date().toISOString().split('T')[0]
    const selecionada = dataSelecionada.value?.toISOString().split('T')[0]
    
    const classes = []
    
    if (dataStr === selecionada) {
        classes.push('bg-blue-500 text-white font-bold')
    } else if (dia.temReservas) {
        classes.push('bg-green-100 border-2 border-green-500 font-semibold text-green-700')
    } else if (dataStr === hoje) {
        classes.push('border-2 border-blue-300 font-semibold')
    } else {
        classes.push('hover:bg-gray-100')
    }
    
    return classes.join(' ')
}

function selecionarDia(dia) {
    if (!dia) return
    dataSelecionada.value = dia.data
}

function mesAnterior() {
    mesAtual.value = new Date(mesAtual.value.getFullYear(), mesAtual.value.getMonth() - 1, 1)
}

function proximoMes() {
    mesAtual.value = new Date(mesAtual.value.getFullYear(), mesAtual.value.getMonth() + 1, 1)
}

const reservasFiltradas = computed(() => {
    let resultado = [...todasReservas.value]
    
    if (dataSelecionada.value) {
        const dataStr = dataSelecionada.value.toISOString().split('T')[0]
        resultado = resultado.filter(reserva => {
            const reservaData = new Date(reserva.data_reserva).toISOString().split('T')[0]
            return reservaData === dataStr
        })
    }
    
    if (filtros.value.rota) {
        resultado = resultado.filter(r => r.rota?.id == filtros.value.rota)
    }
    
    if (filtros.value.suite) {
        resultado = resultado.filter(r => r.suite?.id == filtros.value.suite)
    }
    
    if (filtros.value.status) {
        resultado = resultado.filter(r => r.status_reserva === filtros.value.status)
    }
    
    return resultado
})

function aplicarFiltros() {
    // Os filtros são reativos
}

function limparFiltros() {
    filtros.value.rota = ''
    filtros.value.suite = ''
    filtros.value.status = ''
    dataSelecionada.value = null
}

function formatDate(dateString) {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR')
}

function formatarDataCompleta(date) {
    return date.toLocaleDateString('pt-BR', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    })
}

function formatCurrency(value) {
    if (!value) return '0,00'
    return parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function getStatusLabel(status) {
    const labels = {
        'RESERVADA': 'Reservada',
        'CONFIRMADA': 'Confirmada',
        'UTILIZADA': 'Utilizada',
        'CANCELADA': 'Cancelada',
        'REEMBOLSADA': 'Reembolsada'
    }
    return labels[status] || status
}

function getStatusBadgeClass(status) {
    const classes = {
        'RESERVADA': 'badge badge-info',
        'CONFIRMADA': 'badge badge-success',
        'UTILIZADA': 'badge badge-primary',
        'CANCELADA': 'badge badge-error',
        'REEMBOLSADA': 'badge badge-warning'
    }
    return classes[status] || 'badge'
}

const confirmDelete = (id) => {
    Swal.fire({
        title: 'Tem certeza?',
        text: "Você não poderá reverter isso!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sim, apague!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            router.delete(`/viagens/reservas/${id}/edit`, {
                onSuccess: () => {
                    Swal.fire('Apagado!', 'A reserva foi apagada.', 'success')
                    todasReservas.value = todasReservas.value.filter(r => r.id !== id)
                }
            })
        }
    })
}
</script>

<style scoped>
.aspect-square {
    aspect-ratio: 1 / 1;
}
</style>
