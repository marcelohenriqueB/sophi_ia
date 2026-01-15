<template>
    <div class="border border-gray-200 rounded-2xl py-6 bg-white">
        <div class="px-6 flex justify-between items-center mb-4">
            <div class="flex justify-between">
                <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                    <font-awesome-icon icon="bed" class="text-white" />
                </span>
                <div class="flex flex-col justify-center">
                    <h2 class="text-lg font-medium">Suítes</h2>
                    <p class="text-sm font-normal text-slate-600 my-0">
                        Gerencie as suítes cadastradas na plataforma.
                    </p>
                </div>
            </div>

            <a href="/viagens/suites/create" class="btn btn-primary rounded-2xl">
                <font-awesome-icon icon="plus" class="mr-2" />
                Nova Suíte
            </a>
        </div>

        <hr class="my-4 border-gray-200" />

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <h1 class="text-2xl mb-5">Lista de Suítes</h1>
            <div class="overflow-x-auto">
                <table class="table table-sm w-full">
                    <thead>
                        <tr class="bg-slate-200">
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Passageiros Inclusos</th>
                            <th>Valor</th>
                            <th>Status</th>
                            <th>Data Criação</th>
                            <th>Visualizar</th>
                            <th>Apagar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="suite in suites" :key="suite.id" class="hover:bg-slate-100">
                            <td>{{ suite.id }}</td>
                            <td>{{ suite.nome }}</td>
                            <td>{{ suite.passageiros_inclusos }}</td>
                            <td>R$ {{ formatCurrency(suite.valor) }}</td>
                            <td>
                                <span :class="suite.ativo ? 'badge badge-success' : 'badge badge-error'">
                                    {{ suite.ativo ? 'Ativo' : 'Inativo' }}
                                </span>
                            </td>
                            <td>{{ formatDate(suite.criado_em) }}</td>
                            <td>
                                <Link :href="`/viagens/suites/${suite.id}/edit`" class="btn btn-sm bg-green-500 rounded-2xl">
                                    <font-awesome-icon icon="eye" class="text-white" />
                                </Link>
                            </td>
                            <td>
                                <a :href="`/viagens/suites/${suite.id}/edit`" method="delete"
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
    suites: {
        type: Array,
        required: true
    },
    pagination: {
        type: Object,
        required: true
    }
})

const suites = ref(props.suites)
const pagination = ref(props.pagination)

// Atualiza os dados se props mudarem
watch(
    () => props.suites,
    (newVal) => {
        suites.value = newVal
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
                'A suíte foi apagada.',
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
    router.get(`?page=${page}`, {}, { preserveState: true, replace: true })
}
</script>
