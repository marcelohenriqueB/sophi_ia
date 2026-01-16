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

        <!-- Filtros de Pesquisa -->
        <div class="px-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <!-- Pesquisa por Cliente -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Cliente</label>
                    <input
                        v-model="filtros.cliente"
                        type="text"
                        placeholder="Nome do cliente"
                        class="input input-bordered w-full rounded-lg"
                        @input="pesquisar"
                    />
                </div>

                <!-- Pesquisa por Rota -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Rota</label>
                    <input
                        v-model="filtros.rota"
                        type="text"
                        placeholder="Nome da rota"
                        class="input input-bordered w-full rounded-lg"
                        @input="pesquisar"
                    />
                </div>

                <!-- Filtro por Status de Pagamento -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Status Pagamento</label>
                    <select
                        v-model="filtros.pago"
                        class="select select-bordered w-full rounded-lg"
                        @change="pesquisar"
                    >
                        <option value="">Todos</option>
                        <option value="true">Pago</option>
                        <option value="false">Pendente</option>
                    </select>
                </div>

                <!-- Filtro por Data -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Data Reserva</label>
                    <input
                        v-model="filtros.data"
                        type="date"
                        class="input input-bordered w-full rounded-lg"
                        @change="pesquisar"
                    />
                </div>
            </div>

            <!-- Botão Limpar Filtros -->
            <div class="mt-4">
                <button @click="limparFiltros" class="btn btn-sm btn-outline rounded-lg">
                    <font-awesome-icon icon="filter-circle-xmark" class="mr-2" />
                    Limpar Filtros
                </button>
            </div>
        </div>

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <h1 class="text-2xl mb-5">Lista de Reservas</h1>
            <div class="overflow-x-auto">
                <table class="table table-sm w-full">
                    <thead>
                        <tr class="bg-slate-200">
                            <th>ID</th>
                            <th>Cliente</th>
                            <th>Rota</th>
                            <th>Suíte</th>
                            <th>Valor Total</th>
                            <th>Status Pagamento</th>
                            <th>Data Reserva</th>
                            <th>Data Criação</th>
                            <th>Visualizar</th>
                            <th>Apagar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="reserva in reservas" :key="reserva.id" class="hover:bg-slate-100">
                            <td>{{ reserva.id }}</td>
                            <td>{{ reserva.customer.nome }}</td>
                            <td>{{ reserva.rota.nome }}</td>
                            <td>{{ reserva.suite?.nome }}</td>
                            <td>R$ {{ formatCurrency(reserva.valor_total) }}</td>
                            <td>
                                <span :class="reserva.pago ? 'badge badge-success' : 'badge badge-warning'">
                                    {{ reserva.pago ? 'Pago' : 'Pendente' }}
                                </span>
                            </td>
                            <td>{{ formatDate(reserva.data_reserva) }}</td>
                            <td>{{ formatDate(reserva.criado_em) }}</td>
                            <td>
                                <Link :href="`/viagens/reservas/${reserva.id}/edit`" class="btn btn-sm bg-green-500 rounded-2xl">
                                    <font-awesome-icon icon="eye" class="text-white" />
                                </Link>
                            </td>
                            <td>
                                <a :href="`/viagens/reservas/${reserva.id}/edit`" method="delete"
                                    @click="confirmDelete"
                                    class="btn btn-sm bg-red-500 rounded-2xl">
                                    <font-awesome-icon icon="trash" class="text-white" />
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Paginação -->
            <div class="flex justify-between mt-5">
                <button class="btn btn-sm" :disabled="!pagination.has_previous"
                    @click="changePage(pagination.current_page - 1)">
                    Anterior
                </button>

                <span>Página {{ pagination.current_page }} de {{ pagination.num_pages }}</span>

                <button class="btn btn-sm" :disabled="!pagination.has_next"
                    @click="changePage(pagination.current_page + 1)">
                    Próximo
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { router } from '@inertiajs/vue3'
import { Link } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

const props = defineProps({
    reservas: {
        type: Array,
        required: true
    },
    pagination: {
        type: Object,
        required: true
    },
    filters: {
        type: Object,
        default: () => ({})
    }
})

const reservas = ref(props.reservas)
const pagination = ref(props.pagination)

// Estado dos filtros
const filtros = ref({
    cliente: props.filters?.cliente || '',
    rota: props.filters?.rota || '',
    pago: props.filters?.pago || '',
    data: props.filters?.data || ''
})

// Debounce timer
let debounceTimer = null

// Função de pesquisa com debounce
function pesquisar() {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
        const params = {}
        
        if (filtros.value.cliente) params.cliente = filtros.value.cliente
        if (filtros.value.rota) params.rota = filtros.value.rota
        if (filtros.value.pago !== '') params.pago = filtros.value.pago
        if (filtros.value.data) params.data = filtros.value.data
        
        router.get(window.location.pathname, params, {
            preserveState: true,
            preserveScroll: true,
            replace: true
        })
    }, 500)
}

// Limpar filtros
function limparFiltros() {
    filtros.value = {
        cliente: '',
        rota: '',
        pago: '',
        data: ''
    }
    router.get(window.location.pathname, {}, {
        preserveState: true,
        preserveScroll: true,
        replace: true
    })
}

// Atualiza os dados se props mudarem
watch(
    () => props.reservas,
    (newVal) => {
        reservas.value = newVal
    }
)

// Formata a data
function formatDate(dateString) {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR')
}

// Formata moeda
function formatCurrency(value) {
    if (!value) return '0,00'
    return parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const confirmDelete = (event) => {
    event.preventDefault()

    const url = event.currentTarget.getAttribute('href')

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
            router.delete(url)
            Swal.fire(
                'Apagado!',
                'A reserva foi apagada.',
                'success'
            )
        }
    })
}

watch(
    () => props.pagination,
    (newVal) => {
        pagination.value = newVal
    }
)

// Função para mudar de página
function changePage(page) {
    const params = { page }
    
    // Preservar filtros na mudança de página
    if (filtros.value.cliente) params.cliente = filtros.value.cliente
    if (filtros.value.rota) params.rota = filtros.value.rota
    if (filtros.value.pago !== '') params.pago = filtros.value.pago
    if (filtros.value.data) params.data = filtros.value.data
    
    router.get(window.location.pathname, params, { 
        preserveState: true, 
        replace: true 
    })
}
</script>