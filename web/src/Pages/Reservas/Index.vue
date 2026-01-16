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
                        <!-- Pesquisa por Cliente -->
                        <div>
                            <label class="text-sm font-medium text-gray-700">Cliente</label>
                            <input
                                v-model="filtros.cliente"
                                type="text"
                                placeholder="Nome do cliente"
                                class="input input-bordered w-full mt-1"
                                @input="aplicarFiltros"
                            />
                        </div>

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

                        <!-- Filtro por Status de Pagamento -->
                        <div>
                            <label class="text-sm font-medium text-gray-700">Status Pagamento</label>
                            <select v-model="filtros.pago" @change="aplicarFiltros" 
                                class="select select-bordered w-full mt-1">
                                <option value="">Todos</option>
                                <option value="true">Pago</option>
                                <option value="false">Pendente</option>
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

                <div v-else-if="reservas.length === 0" class="text-center py-12">
                    <font-awesome-icon icon="inbox" class="text-6xl text-gray-300 mb-4" />
                    <p class="text-gray-500">Nenhuma reserva encontrada</p>
                </div>

                <div v-else>
                    <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
                        <div v-for="reserva in reservas" :key="reserva.id" class="border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-all bg-white">
                            <div class="flex items-start justify-between mb-3">
                                <div>
                                    <p class="text-xs text-slate-500">Reserva #{{ reserva.id }}</p>
                                    <h3 class="text-lg font-semibold text-slate-800">{{ reserva.customer?.nome || 'Cliente não informado' }}</h3>
                                </div>
                                <div class="flex flex-col items-end gap-1 ">
                                    <span :class="reserva.pago ? 'badge badge-success' : 'badge badge-warning'">
                                        <span class="text[9px]">
                                            {{ reserva.pago ? 'Pago' : 'Pendente' }}
                                        </span> 
                                    </span>
                                    <span :class="getStatusBadgeClass(reserva.status_reserva)">
                                        <span class="text-[9px]">
                                        {{ getStatusLabel(reserva.status_reserva) }}
                                        </span>
                                    </span>
                                </div>
                            </div>

                            <div class="space-y-2 text-sm text-slate-700">
                                <div class="flex items-center justify-between">
                                    <span class="font-medium text-slate-600">Rota</span>
                                    <span>{{ reserva.rota?.nome || '-' }}</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="font-medium text-slate-600">Suíte</span>
                                    <span>{{ reserva.suite?.nome || '-' }}</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="font-medium text-slate-600">Data</span>
                                    <span>{{ formatDate(reserva.data_reserva) }}</span>
                                </div>
                                <div class="flex items-center justify-between">
                                    <span class="font-medium text-slate-600">Valor</span>
                                    <span class="text-base font-semibold text-emerald-700">R$ {{ formatCurrency(reserva.valor_total) }}</span>
                                </div>
                            </div>

                            <div class="flex items-center justify-between mt-4 gap-2 flex-wrap">
                                <div class="flex gap-2">
                                    <Link :href="`/viagens/reservas/${reserva.id}/edit`" class="btn btn-sm bg-slate-800 text-white rounded-lg">
                                        <font-awesome-icon icon="eye" class="mr-2" /> Ver detalhes
                                    </Link>
                                    <button @click="showQr(reserva)" class="btn btn-sm btn-outline rounded-lg">
                                        <font-awesome-icon icon="qrcode" class="mr-1" /> QR Embarque
                                    </button>
                                </div>
                                <button @click="confirmDelete(reserva.id)" class="btn btn-sm bg-red-500 text-white rounded-lg">
                                    <font-awesome-icon icon="trash" class="mr-1" /> Excluir
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="flex justify-between items-center mt-6" v-if="pagination">
                        <div class="text-sm text-slate-600">
                            Página {{ pagination.current_page }} de {{ pagination.num_pages }} · Total {{ pagination.total }}
                        </div>
                        <div class="flex gap-2">
                            <button class="btn btn-sm" :disabled="!pagination.has_previous" @click="goToPage(pagination.current_page - 1)">
                                Anterior
                            </button>
                            <button class="btn btn-sm" :disabled="!pagination.has_next" @click="goToPage(pagination.current_page + 1)">
                                Próxima
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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
    },
    pagination: {
        type: Object,
        default: () => null
    },
    filters: {
        type: Object,
        default: () => ({})
    },
    reserved_dates: {
        type: Array,
        default: () => []
    }
})

const diasSemana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

const mesAtual = ref(new Date())
const dataSelecionada = ref(props.filters?.data ? new Date(props.filters.data) : null)
const carregando = ref(false)
const rotas = ref(props.rotas)
const suites = ref(props.suites)
const reservas = computed(() => props.reservas ?? [])
const pagination = computed(() => props.pagination || null)

const filtros = ref({
    cliente: props.filters?.cliente || '',
    rota: props.filters?.rota || '',
    suite: props.filters?.suite || '',
    pago: props.filters?.pago || '',
    status: props.filters?.status || '',
    data: props.filters?.data || ''
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
    return props.reserved_dates?.includes(dataStr)
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
    aplicarFiltros()
}

function mesAnterior() {
    mesAtual.value = new Date(mesAtual.value.getFullYear(), mesAtual.value.getMonth() - 1, 1)
}

function proximoMes() {
    mesAtual.value = new Date(mesAtual.value.getFullYear(), mesAtual.value.getMonth() + 1, 1)
}

function aplicarFiltros() {
    filtros.value.data = dataSelecionada.value ? dataSelecionada.value.toISOString().split('T')[0] : ''
    fetchReservas(1)
}

    
function limparFiltros() {
    filtros.value.rota = ''
    filtros.value.suite = ''
    filtros.value.status = ''
    dataSelecionada.value = null
    filtros.value.cliente = ''
    filtros.value.pago = ''
    filtros.value.data = ''
    fetchReservas(1)
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
        'AGUARDANDO_PAGAMENTO': 'Aguardando Pagamento',
        'PAGAMENTO_CONFIRMADO': 'Pagamento Confirmado',
        'AGUARDANDO_EMBARQUE': 'Aguardando Embarque',
        'EMBARCADO': 'Embarcado',
        'CANCELADA': 'Cancelada',
        'REEMBOLSADA': 'Reembolsada'
    }
    return labels[status] || status
}

function getStatusBadgeClass(status) {
    const classes = {
        'AGUARDANDO_PAGAMENTO': 'badge badge-warning',
        'PAGAMENTO_CONFIRMADO': 'badge badge-info',
        'AGUARDANDO_EMBARQUE': 'badge badge-primary',
        'EMBARCADO': 'badge badge-success',
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
                    const currentPage = pagination.value?.current_page || 1
                    fetchReservas(currentPage)
                }
            })
        }
    })
}

function buildPublicLink(reserva) {
    const base = typeof window !== 'undefined' ? window.location.origin : ''
    return `${base}/viagens/reservas/public/${reserva.embarque_uuid}`
}

function showQr(reserva) {
    const link = buildPublicLink(reserva)
    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=260x260&data=${encodeURIComponent(link)}`
    const cliente = reserva.customer?.nome || 'Cliente'
    const rota = reserva.rota?.nome || '-'
    const status = getStatusLabel(reserva.status_reserva)

    Swal.fire({
        title: 'QR de embarque',
        html: `
            <div class="flex flex-col items-center gap-3">
                <img src="${qrUrl}" alt="QR de embarque" class="rounded-lg border border-gray-200" />
                <div class="text-sm font-semibold text-slate-800">${cliente}</div>
                <div class="text-xs text-slate-600">Rota: ${rota}</div>
                <div class="text-xs text-slate-600">Status: ${status}</div>
                <div class="text-[11px] text-slate-500 break-words max-w-xs">${link}</div>
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Fechar',
        cancelButtonText: 'Copiar link',
        customClass: {
            popup: 'rounded-2xl'
        }
    }).then(async (result) => {
        if (result.dismiss === Swal.DismissReason.cancel) {
            try {
                await navigator.clipboard.writeText(link)
                Swal.fire('Copiado!', 'Link copiado para a área de transferência.', 'success')
            } catch (err) {
                Swal.fire('Erro', 'Não foi possível copiar o link.', 'error')
            }
        }
    })
}

function fetchReservas(page = 1) {
    carregando.value = true
    router.get('/viagens/reservas/list', {
        ...filtros.value,
        page
    }, {
        preserveScroll: true,
        preserveState: true,
        replace: true,
        onFinish: () => {
            carregando.value = false
        }
    })
}

function goToPage(page) {
    const pageInfo = pagination.value
    if (!pageInfo) return
    const nextPage = Math.max(1, Math.min(page, pageInfo.num_pages))
    fetchReservas(nextPage)
}

watch(() => props.filters, (novosFiltros) => {
    filtros.value = {
        cliente: novosFiltros?.cliente || '',
        rota: novosFiltros?.rota || '',
        suite: novosFiltros?.suite || '',
        pago: novosFiltros?.pago || '',
        status: novosFiltros?.status || '',
        data: novosFiltros?.data || ''
    }
    dataSelecionada.value = novosFiltros?.data ? new Date(novosFiltros.data) : null
})
</script>

<style scoped>
.aspect-square {
    aspect-ratio: 1 / 1;
}
</style>
