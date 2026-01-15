<template>
    <form @submit="submit" class="border border-gray-200 rounded-2xl py-6 bg-white" action="/viagens/clientes/create"
        method="post">
        <div class="flex px-6">
            <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                <font-awesome-icon icon="user" class="text-white" />
            </span>
            <div class="flex flex-col justify-center">
                <h2 class="text-lg font-medium">Editar Cliente ID: {{ form.id }}</h2>
                <p class="text-sm font-normal text-slate-600 my-0">Atualize os detalhes do cliente.</p>
            </div>
        </div>
        <hr class="my-4 border-gray-200" />

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <div>
                <span class="text-sm uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="user-circle" class="" />
                    Informações Pessoais
                </span>
            </div>

            <div class="flex flex-col gap-2 w-full">
                <label for="">
                    Nome Completo <span class="text-red-500">*</span>
                </label>
                <label class="input rounded-2xl">
                    <input type="text" v-model="form.nome" placeholder="Ex: João Silva" name="nome" required />
                    <font-awesome-icon icon="user" class="text-gray-500" />
                </label>
            </div>

            <div class="flex flex-col gap-2 w-full">
                <label for="">
                    Email <span class="text-red-500">*</span>
                </label>
                <label class="input rounded-2xl">
                    <input type="email" v-model="form.email" placeholder="Ex: joao@example.com" name="email" required />
                    <font-awesome-icon icon="envelope" class="text-gray-500" />
                </label>
            </div>

            <div class="flex flex-col gap-2 w-full mt-3">
                <span class="text-sm uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="info-circle" class="" />
                    Informações de Contato
                </span>
            </div>

            <div class="flex gap-10 w-full">
                <div class="flex flex-col gap-2 flex-1">
                    <label for="">
                        Telefone
                    </label>
                    <label class="input rounded-2xl">
                        <input type="tel" v-model="form.telefone" placeholder="Ex: (92) 99999-9999" name="telefone" />
                        <font-awesome-icon icon="phone" class="text-gray-500" />
                    </label>
                </div>

                <div class="flex flex-col gap-2 flex-1">
                    <label for="">
                        CPF/CNPJ
                    </label>
                    <label class="input rounded-2xl">
                        <input type="text" v-model="form.cpf_cnpj" placeholder="Ex: 123.456.789-10" name="cpf_cnpj" />
                        <font-awesome-icon icon="id-card" class="text-gray-500" />
                    </label>
                </div>
            </div>

            <div class="flex justify-start mt-8">
                <button class="btn bg-amber-500 shadow-none text-white rounded-2xl px-6">
                    Atualizar Cliente
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import { useForm } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

const props = defineProps({
    cliente: Object
})

const form = useForm({
    id: props.cliente.id || null,
    nome: props.cliente.nome || '',
    email: props.cliente.email || '',
    telefone: props.cliente.telefone || '',
    cpf_cnpj: props.cliente.cpf_cnpj || '',
})

function submit(e) {
    e.preventDefault()
    form.post(`/viagens/clientes/${props.cliente.id}/edit`, {
        onSuccess: () => {
            Swal.fire({
                icon: 'success',
                title: 'Cliente atualizado com sucesso!',
                showConfirmButton: false,
                timer: 1500
            })
        },
        onError: (errors) => {
            const mensagem = Object.entries(errors)
                .map(([campo, msgs]) => `${campo}: ${msgs.join(', ')}`)
                .join('\n')
            
            Swal.fire({
                icon: 'error',
                title: 'Erro ao atualizar o cliente',
                text: mensagem,
            })
        },
    })
}
</script>