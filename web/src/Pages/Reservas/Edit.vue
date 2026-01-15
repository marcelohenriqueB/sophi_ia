<template>
    <form @submit="submit" class="border border-gray-200 rounded-2xl py-6 bg-white" method="post">
        <div class="flex px-6">
            <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                <font-awesome-icon icon="calendar-check" class="text-white" />
            </span>
            <div class="flex flex-col justify-center">
                <h2 class="text-lg font-medium">Editar Reserva ID: {{ reserva.id }}</h2>
                <p class="text-sm font-normal text-slate-600 my-0">Atualize os detalhes da reserva.</p>
            </div>

            
        </div>
        <hr class="my-4 border-gray-200" />

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <!-- Seção: Informações da Reserva -->
            <div class="flex justify-between">
                <span class="text-sm uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="info-circle" />
                    Informações da Reserva
                </span>

                <div class="flex gap-2">
                    <a class="btn btn-info rounded-2xl text-white" :href="reserva.cobranca_asaas_link" target="_blank" rel="noopener noreferrer">
                        <font-awesome-icon icon="link" class="mr-2" />
                        Link da Cobrança
                    </a>

                    <img
                    v-if="reserva.qr_code_pix"
                    :src="`data:image/png;base64,${reserva.qr_code_pix}`"
                    alt="QR Code PIX"
                    class="w-32 h-32"
                    />                
                </div>
                
            </div>
            
            <div class="flex gap-10 w-full">
                <div class="flex flex-col gap-2 flex-1">
                    <label for="customer">
                        Cliente <span class="text-red-500">*</span>
                    </label>
                    <select v-model="form.customer_id" class="select select-bordered rounded-2xl" required>
                        <option value="">Selecione um cliente</option>
                        <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                            {{ cliente.nome }}
                        </option>
                    </select>
                </div>

                

                <div class="flex flex-col gap-2 flex-1">
                    <label for="rota">
                        Rota <span class="text-red-500">*</span>
                    </label>
                    <select v-model="form.rota_id" class="select select-bordered rounded-2xl" required>
                        <option value="">Selecione uma rota</option>
                        <option v-for="rota in rotas" :key="rota.id" :value="rota.id">
                            {{ rota.nome }} - {{ rota.saindo_de }} → {{ rota.indo_para }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="flex gap-10 w-full">
                <div class="flex flex-col gap-2 flex-1">
                    <label for="suite">
                        Suíte <span class="text-red-500">*</span>
                    </label>
                    <select v-model="form.suite_id" @change="onSuiteChange" class="select select-bordered rounded-2xl" required>
                        <option value="">Selecione uma suíte</option>
                        <option v-for="suite in suites" :key="suite.id" :value="suite.id">
                            {{ suite.nome }} - R$ {{ formatCurrency(suite.valor) }}
                        </option>
                    </select>
                    <p v-if="suiteSelecionada" class="text-sm text-gray-600">
                        Passageiros inclusos: {{ suiteSelecionada.passageiros_inclusos }}
                    </p>
                </div>

                <div class="flex flex-col gap-2 flex-1">
                    <label for="data_reserva">
                        Data do Agendamento <span class="text-red-500">*</span>
                    </label>
                    <label class="input rounded-2xl">
                        <input type="date" v-model="form.data_reserva" name="data_reserva" required />
                        <font-awesome-icon icon="calendar" class="text-gray-500" />
                    </label>
                </div>
            </div>

            <div class="flex gap-10 w-full">
                <div class="flex flex-col gap-2 flex-1">
                    <label for="valor_total">
                        Valor Total (R$)
                    </label>
                    <label class="input rounded-2xl bg-gray-100">
                        <input type="text" :value="formatCurrency(valorTotal)" readonly class="bg-gray-100" />
                        <font-awesome-icon icon="dollar-sign" class="text-gray-500" />
                    </label>
                </div>

                <div class="flex flex-col gap-2 flex-1">
                    <label for="status_reserva">
                        Status da Reserva
                    </label>
                    <select v-model="form.status_reserva" class="select select-bordered rounded-2xl">
                        <option value="RESERVADA">Reservada</option>
                        <option value="CONFIRMADA">Confirmada</option>
                        <option value="UTILIZADA">Utilizada</option>
                        <option value="CANCELADA">Cancelada</option>
                        <option value="REEMBOLSADA">Reembolsada</option>
                    </select>
                </div>
            </div>

            <div class="flex gap-10 w-full">
                <div class="flex flex-col gap-2 flex-1">
                    <!-- Espaço vazio -->
                </div>

                <div class="flex flex-col gap-2 flex-1">
                    <label class="flex items-center gap-2 cursor-pointer">
                        <input type="checkbox" v-model="form.pago" class="checkbox" name="pago" />
                        <span class="label-text">Pagamento Realizado</span>
                    </label>
                </div>
            </div>

            <!-- Seção: Passageiros -->
            <div class="mt-6">
                <span class="text-sm uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="users" />
                    Passageiros
                </span>
            </div>

            <div class="border border-gray-300 rounded-2xl p-4">
                <div v-for="(passageiro, index) in form.passageiros" :key="index" class="mb-4 pb-4 border-b border-gray-200 last:border-b-0">
                    <div class="flex justify-between items-center mb-3">
                        <h3 class="font-medium">Passageiro {{ index + 1 }}</h3>
                        <button type="button" @click="removerPassageiro(index)" 
                            class="btn btn-sm btn-error rounded-2xl">
                            <font-awesome-icon icon="trash" />
                        </button>
                    </div>

                    <div class="flex gap-4">
                        <div class="flex flex-col gap-2 flex-1">
                            <label>Nome Completo <span class="text-red-500">*</span></label>
                            <input type="text" v-model="passageiro.nome" 
                                class="input input-bordered rounded-2xl" 
                                placeholder="Ex: João Silva" required />
                        </div>

                        <div class="flex flex-col gap-2 flex-1">
                            <label>Documento (CPF/RG) <span class="text-red-500">*</span></label>
                            <input type="text" v-model="passageiro.documento" 
                                class="input input-bordered rounded-2xl" 
                                placeholder="Ex: 123.456.789-10" required />
                        </div>

                        <div class="flex flex-col gap-2 flex-1">
                            <label>Data de Nascimento</label>
                            <input type="date" v-model="passageiro.data_nascimento" 
                                class="input input-bordered rounded-2xl" />
                        </div>
                    </div>
                </div>

                <button type="button" @click="adicionarPassageiro" 
                    class="btn btn-outline btn-primary rounded-2xl mt-4 w-full">
                    <font-awesome-icon icon="plus" class="mr-2" />
                    Adicionar Passageiro
                </button>
            </div>

            <!-- Resumo do Valor -->
            <div class="alert alert-info mt-4" v-if="suiteSelecionada">
                <div class="flex flex-col gap-1">
                    <p class="font-medium">Resumo do Valor:</p>
                    <p class="text-sm">
                        Valor da Suíte: R$ {{ formatCurrency(suiteSelecionada.valor) }}
                    </p>
                    <p class="text-sm">
                        Passageiros inclusos: {{ suiteSelecionada.passageiros_inclusos }}
                    </p>
                    <p class="text-sm">
                        Total de passageiros: {{ form.passageiros.length }}
                    </p>
                    <p class="text-sm">
                        Passageiros adicionais: {{ passageirosAdicionais }}
                        <span v-if="passageirosAdicionais > 0">
                            (R$ {{ formatCurrency(suiteSelecionada.valor_passageiro_adicional || (parseFloat(suiteSelecionada.valor || 0) * 0.3)) }} cada = R$ {{ formatCurrency(valorPassageirosAdicionais) }})
                        </span>
                    </p>
                    <p class="text-lg font-bold mt-2">
                        Total: R$ {{ formatCurrency(valorTotal) }}
                    </p>
                </div>
            </div>

            <div class="flex justify-start mt-8">
                <button type="submit" class="btn bg-amber-500 shadow-none text-white rounded-2xl px-6">
                    Atualizar Reserva
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useForm } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

const props = defineProps({
    reserva: Object,
    clientes: Array,
    rotas: Array,
    suites: Array,
    passageiros: Array,
})

console.log(props.passageiros)
const form = useForm({
    customer_id: props.reserva.customer?.id || '',
    rota_id: props.reserva.rota?.id || '',
    suite_id: props.reserva.suite?.id || '',
    data_reserva: props.reserva.data_reserva || '',
    status_reserva: props.reserva.status_reserva || 'RESERVADA',
    pago: props.reserva.pago || false,
    passageiros: props.passageiros || [],
})

const suiteSelecionada = ref(null)

// Inicializa a suíte selecionada
onMounted(() => {
    if (form.suite_id) {
        suiteSelecionada.value = props.suites.find(s => s.id == form.suite_id)
    }
    
    // Carrega os passageiros existentes
    if (props.reserva.passageiros && props.reserva.passageiros.length > 0) {
        form.passageiros = props.reserva.passageiros.map(p => ({
            id: p.id,
            nome: p.nome,
            documento: p.documento,
            data_nascimento: p.data_nascimento || ''
        }))
    } else {
        // Se não tem passageiros, adiciona um vazio
        // adicionarPassageiro()
    }
})

// Calcula quantos passageiros são adicionais (além dos inclusos na suíte)
const passageirosAdicionais = computed(() => {
    if (!suiteSelecionada.value) return 0
    const total = form.passageiros.length
    const inclusos = suiteSelecionada.value.passageiros_inclusos
    return Math.max(0, total - inclusos)
})

// Calcula o valor dos passageiros adicionais
const valorPassageirosAdicionais = computed(() => {
    if (!suiteSelecionada.value) return 0
    // Usa o valor configurado na suíte ou 30% do valor da suíte como fallback
    const valorPorPassageiro = parseFloat(suiteSelecionada.value.valor_passageiro_adicional || 0)
    if (valorPorPassageiro > 0) {
        return passageirosAdicionais.value * valorPorPassageiro
    }
    // Fallback: 30% do valor da suíte por passageiro adicional
    const valorBase = parseFloat(suiteSelecionada.value.valor || 0)
    return passageirosAdicionais.value * (valorBase * 0.3)
})

// Calcula o valor total
const valorTotal = computed(() => {
    if (!suiteSelecionada.value) return 0
    const valorSuite = parseFloat(suiteSelecionada.value.valor || 0)
    return valorSuite + valorPassageirosAdicionais.value
})

// Quando a suíte é alterada
function onSuiteChange() {
    const suiteId = form.suite_id
    if (suiteId) {
        suiteSelecionada.value = props.suites.find(s => s.id == suiteId)
    } else {
        suiteSelecionada.value = null
    }
}

// Adiciona um novo passageiro
function adicionarPassageiro() {
    form.passageiros.push({
        nome: '',
        documento: '',
        data_nascimento: ''
    })
}

// Remove um passageiro
function removerPassageiro(index) {
    form.passageiros.splice(index, 1)
}

// Formata moeda
function formatCurrency(value) {
    if (!value) return '0,00'
    return parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function submit(e) {
    e.preventDefault()

    if (form.passageiros.length === 0) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Adicione pelo menos um passageiro!',
        })
        return
    }

    // Adiciona o valor total ao form
    const formData = {
        ...form.data(),
        valor_total: valorTotal.value.toFixed(2)
    }

    form.transform(() => formData).post(`/viagens/reservas/${props.reserva.id}/edit`, {
        onSuccess: () => {
            Swal.fire({
                icon: 'success',
                title: 'Reserva atualizada com sucesso!',
                showConfirmButton: false,
                timer: 1500
            })
        },
        onError: (errors) => {
            const errorMessages = Object.values(errors).flat().join('\n')
            Swal.fire({
                icon: 'error',
                title: 'Erro ao atualizar reserva',
                text: errorMessages,
            })
        },
    })
}
</script>
