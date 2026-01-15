<template>
    <form @submit="submit" class="border border-gray-200 rounded-2xl py-6 bg-white" action="/viagens/suites/create"
        method="post">
        <div class="flex px-6">
            <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                <font-awesome-icon icon="bed" class="text-white" />
            </span>
            <div class="flex flex-col justify-center">
                <h2 class="text-lg font-medium">Nova Suíte</h2>
                <p class="text-sm font-normal text-slate-600 my-0">Preencha os detalhes da sua nova suíte.</p>
            </div>
        </div>
        <hr class="my-4 border-gray-200" />

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <div>
                <span class="text-sm uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="info-circle" class="" />
                    Informações da Suíte
                </span>
            </div>

            <div class="flex flex-col gap-2 w-full">
                <label for="">
                    Nome da Suíte <span class="text-red-500">*</span>
                </label>
                <label class="input rounded-2xl">
                    <input type="text" v-model="form.nome" placeholder="Ex: Suíte Luxo" name="nome" required />
                    <font-awesome-icon icon="bed" class="text-gray-500" />
                </label>
            </div>

            <div class="flex gap-10 w-full">
                

                <div class="flex flex-col gap-2 flex-1">
                    <label for="">
                        Passageiros Inclusos <span class="text-red-500">*</span>
                    </label>
                    <label class="input rounded-2xl">
                        <input type="number" v-model="form.passageiros_inclusos" placeholder="Ex: 4" 
                            name="passageiros_inclusos" required />
                        <font-awesome-icon icon="users" class="text-gray-500" />
                    </label>
                </div>
            </div>

            <div class="flex gap-10 w-full">
                <div class="flex flex-col gap-2 flex-1">
                    <label for="">
                        Valor (R$) <span class="text-red-500">*</span>
                    </label>
                    <label class="input rounded-2xl">
                        <input type="number" step="0.01" v-model="form.valor" placeholder="Ex: 1500.00" 
                            name="valor" required />
                        <font-awesome-icon icon="dollar-sign" class="text-gray-500" />
                    </label>
                </div>

                <div class="flex flex-col gap-2 flex-1">
                    <label for="">
                        Valor por Passageiro Adicional (R$)
                    </label>
                    <label class="input rounded-2xl">
                        <input type="number" step="0.01" v-model="form.valor_passageiro_adicional" placeholder="Ex: 100.00" 
                            name="valor_passageiro_adicional" />
                        <font-awesome-icon icon="dollar-sign" class="text-gray-500" />
                    </label>
                    <p class="text-xs text-gray-500">Valor cobrado por passageiro além dos inclusos</p>
                </div>
            </div>
            <div>
                <div class="flex flex-col gap-2 flex-1">
                    <label class="flex items-center gap-2 cursor-pointer">
                        <input type="checkbox" v-model="form.ativo" class="checkbox" name="ativo" />
                        <span class="label-text">Suíte Ativa</span>
                    </label>
                </div>
            </div>
            <div class="flex justify-start mt-8">
                <button class="btn bg-purple-500 shadow-none text-white rounded-2xl px-6">
                    Criar Suíte
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import { useForm } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

const form = useForm({
    nome: '',
    capacidade_toneladas: 0,
    passageiros_inclusos: 0,
    valor: 0,
    valor_passageiro_adicional: 0,
    ativo: true,
})

function submit(e) {
    e.preventDefault()
    form.post('/viagens/suites/create', {
        onSuccess: () => {
            console.log('Suíte criada com sucesso!')
            Swal.fire({
                icon: 'success',
                title: 'Suíte criada com sucesso!',
                showConfirmButton: false,
                timer: 1500
            })
        },
        onError: (errors) => {
            const errorMessages = Object.values(errors).flat().join('\n')
            Swal.fire({
                icon: 'error',
                title: 'Erro ao criar suíte',
                text: errorMessages,
            })

        },
        forceFormData: true
    })
}
</script>
