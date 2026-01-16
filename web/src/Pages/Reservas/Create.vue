<template>
    <form @submit="submit" class="border border-gray-200 rounded-2xl py-6 bg-white" method="post">
        <div class="flex px-6">
            <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                <font-awesome-icon icon="calendar-check" class="text-white" />
            </span>
            <div class="flex flex-col justify-center">
                <h2 class="text-lg font-medium">Nova Reserva</h2>
                <p class="text-sm font-normal text-slate-600 my-0">Preencha os detalhes da nova reserva.</p>
            </div>
        </div>
        <hr class="my-4 border-gray-200" />

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <!-- Seção: Informações da Reserva -->
            <div>
                <span class="text-sm uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="info-circle" />
                    Informações da Reserva
                </span>
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
                        Rota 
                    </label>
                    <select v-model="form.rota_id" class="select select-bordered rounded-2xl" >
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
                        Suíte 
                    </label>
                    <select v-model="form.suite_id" @change="onSuiteChange" class="select select-bordered rounded-2xl" >
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
                        <option value="AGUARDANDO_PAGAMENTO">Aguardando Pagamento</option>
                        <option value="PAGAMENTO_CONFIRMADO">Pagamento Confirmado</option>
                        <option value="AGUARDANDO_EMBARQUE">Aguardando Embarque</option>
                        <option value="EMBARCADO">Embarcado</option>
                        <option value="CANCELADA">Cancelada</option>
                        <option value="REEMBOLSADA">Reembolsada</option>
                    </select>
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

                        <div class="d-flex gap-2 flex-1" v-if="suiteSelecionada && suiteSelecionada.passageiros_inclusos > 0 && form.passageiros.filter(p => p.suite).length < suiteSelecionada.passageiros_inclusos || passageiro.suite">
                            <label class="cursor-pointer flex items-center gap-2 mt-6">
                                <input type="checkbox" @click="passageiro.suite = !passageiro.suite" class="checkbox checkbox-primary" />
                                Suíte Inclusa (Passagem gratuita) 
                            </label>
                        </div>

                        <div class="flex flex-col gap-2 flex-1">
                            <!-- Espaço vazio para manter alinhamento -->
                            <label class="cursor-pointer flex items-center gap-2 mt-6">
                                <input type="checkbox" v-model="passageiro.pcd" class="checkbox checkbox-primary" />
                                Possui Desconto PCD
                            </label>
                        </div>
                    </div>
                </div>

                <button type="button" @click="adicionarPassageiro" 
                    class="btn btn-outline btn-primary rounded-2xl mt-4 w-full">
                    <font-awesome-icon icon="plus" class="mr-2" />
                    Adicionar Passageiro
                </button>
            </div>

            
            <div class="flex justify-start mt-8">
                <button type="submit" class="btn bg-purple-500 shadow-none text-white rounded-2xl px-6">
                    Criar Reserva
                </button>
            </div>
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useForm } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

interface Passageiro {
    nome: string
    documento: string
    data_nascimento: string
    desconto?: number
    suite?: boolean
    pcd: boolean
}
interface ConfigViagem {
    desconto_idoso: number
    desconto_crianca_5_7: number
    desconto_crianca_8_10: number
    desconto_acima_11: number
    desconto_crianca_0_4: number
    desconto_pcd: number
    
}
interface Rota {
    id: string
    nome: string
    valor: number
    saindo_de: string
    indo_para: string
    
}
class Customer {
    id!: string
    nome!: string
}
interface Suite {
    id: string
    nome: string
    valor: number
    passageiros_inclusos: number
}

const props = defineProps({
    clientes:   Array as () => Customer[],
    rotas: {
        type: Array as () => Rota[],
        required: true
    },
    suites: {
        type: Array as () => Suite[],
        required: true
    },
    config_viagem: {
        type: Object as () => ConfigViagem,
        required: true
    },
})


const form = useForm({
    customer_id:'',
    rota_id: '',
    suite_id: '',
    data_reserva: '',
    status_reserva: 'AGUARDANDO_PAGAMENTO',
    passageiros: [] as Passageiro[],
})


const suiteSelecionada = ref(null as  null | Suite)

// Calcula o valor dos passageiros adicionais

// Calcula o valor total
const valorTotal = computed(() => {
    
    const valorSuite = suiteSelecionada.value ? parseFloat(suiteSelecionada.value?.valor.toString() ?? 0) : 0

    const valorRota = form.rota_id ? (() => {
        const rota = props.rotas?.find(r => r.id == form.rota_id)
        return rota ? parseFloat(rota.valor.toString() ?? 0) : 0
    })() : 0

    // 

    // calcular o desconto
    
    const pegarPassageirosSemSuite = form.passageiros.filter(p => !p.suite);


    const total = pegarPassageirosSemSuite.reduce((acc, passageiro) => {
        let desconto = 0;

        // Verifica e aplica descontos
        if (passageiro.pcd) {
            desconto += props.config_viagem.desconto_pcd || 0;
        }
        // calcula idade se data de nascimento for fornecida
        if (passageiro.data_nascimento) {
            const nascimento = new Date(passageiro.data_nascimento);
            const hoje = new Date();
            let idade = hoje.getFullYear() - nascimento.getFullYear();
            const mes = hoje.getMonth() - nascimento.getMonth();
            if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
                idade--;
            }

            if (idade >= 5 && idade <= 7) {
                desconto += props.config_viagem.desconto_crianca_5_7 || 0;
            } else if (idade >= 8 && idade <= 10) {
                desconto += props.config_viagem.desconto_crianca_8_10 || 0;
            } else if (idade >= 0 && idade <= 4) {
                desconto += props.config_viagem.desconto_crianca_0_4 || 0;
            } else if (idade >= 11  && idade <= 17) {
                desconto += props.config_viagem.desconto_acima_11 || 0;
            }
        }

        // Aqui você pode adicionar mais condições para outros tipos de desconto
        // Exemplo: idade, etc.

        const valorComDesconto = valorRota * (1 - desconto / 100);
        return acc + valorComDesconto;
    }, 0);
    return total + valorSuite;
    


})

// Quando a suíte é alterada
function onSuiteChange() {
    const suiteId = form.suite_id
    if (suiteId) {
        suiteSelecionada.value = props.suites.find(suite => suite.id === suiteId) || null
    } else {
        suiteSelecionada.value = null
    }
}

// Adiciona um novo passageiro
function adicionarPassageiro() {
    form.passageiros.push({
        nome: '',
        documento: '',
        data_nascimento: '',
        pcd: false,
    })
}

// Remove um passageiro
function removerPassageiro(index: number) {
    form.passageiros.splice(index, 1)
}

// Formata moeda
function formatCurrency(value: number) {
    if (!value) return '0,00'
    return parseFloat(value.toString()).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function submit(e: Event) {
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

    form.transform(() => formData).post('/viagens/reservas/create', {
        onSuccess: () => {
            Swal.fire({
                icon: 'success',
                title: 'Reserva criada com sucesso!',
                showConfirmButton: false,
                timer: 1500
            })
        },
        onError: (errors) => {
            const errorMessages = Object.values(errors).flat().join('\n')
            Swal.fire({
                icon: 'error',
                title: 'Erro ao criar reserva',
                text: errorMessages,
            })
        },

    })
}

// Adiciona um passageiro inicial
adicionarPassageiro()
</script>
