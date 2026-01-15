<template>
    <form @submit="submit" class="border border-gray-200 rounded-2xl py-6 bg-white" action="/viagens/rotas/create"
        method="post">
        <div class="flex px-6">
            <span class="px-3 py-4 bg-slate-600 text-white rounded-2xl mr-2 text-2xl font-bold">
                <font-awesome-icon icon="map-location" class=" text-white" />
            </span>
            <div class="flex flex-col justify-center">
                <h2 class="text-lg font-medium">Editar Rota de viagem  Id: {{ form.id }}</h2>
                <p class="text-sm font-normal text-slate-600 my-0">Preencha os detalhes da sua rota de viagem.</p>
            </div>
        </div>
        <hr class="my-4 border-gray-200" />

        <div class="px-6 flex flex-col gap-4 md:w-full mt-10">
            <div>
                <span class="text-sm  uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="map-location" class="" />
                    Intinerário da viagem
                </span>
            </div>

            <div class="flex flex-col gap-2 w-full">
                <label for="">
                    Nome da Rota <span class="text-red-500">*</span>
                </label>
                <label class="input rounded-2xl">
                    <input type="text" v-model="form.nome" placeholder="Ex: Rota Amazônica" name="nome" />
                    <font-awesome-icon icon="map-location" class="text-gray-500" />
                </label>
            </div>
            <div class="flex mt-3 flex-col gap-4">
                <div class="flex gap-10 w-full">
                    <div class="flex flex-col gap-2">
                        <label for="">
                            Origem <span class="text-red-500">*</span>
                        </label>
                        <label class="input rounded-2xl">
                            <input type="text" required v-model="form.saindo_de" placeholder="Ex: Manaus"
                                name="saindo_de" />
                            <font-awesome-icon icon="map-location" class="text-gray-500" />
                        </label>
                    </div>

                    <div class="flex flex-col gap-2">
                        <label for="">
                            Destino <span class="text-red-500">*</span>
                        </label>
                        <label class="input  rounded-2xl">
                            <input type="text" required v-model="form.indo_para" placeholder="Ex: Manaus"
                                name="indo_para" />
                            <font-awesome-icon icon="map-location" class="text-gray-500" />
                        </label>
                    </div>
                </div>

                <hr class="my-4 border-gray-200" />

                <span class="text-sm  uppercase font-medium text-gray-500 flex items-center gap-2">
                    <font-awesome-icon icon="clock" class="" />
                    Detalhes da Operacional
                </span>

                <div class="flex gap-10 w-full">
                    <div class="flex flex-col  gap-2">
                        <label for="">
                            Horário de partida <span class="text-red-500">*</span>
                        </label>
                        <input type="time" class="input rounded-2xl" required v-model="form.horario_partida" placeholder="Ex: 08:00"
                            name="horario_partida" 
                        />
                    </div>
                </div>
                <div class="flex gap-5  w-full mt-4">
                    <div class="flex flex-col">
                        <label for="">
                            Status da rota <span class="text-red-500">*</span>
                        </label>
                        <div class="border border-gray-300 rounded-2xl px-4 py-2 flex items-center w-60">
                            <input type="checkbox" class="toggle toggle-sm" v-model="form.ativo" name="ativo" />
                        </div>
                    </div>
                    <div class="flex flex-col">
                        <label for="">
                            Capacidade Diária <span class="text-red-500">*</span>
                        </label>
                        <label class="input rounded-2xl w-60">
                            <input type="number" required v-model="form.capacidade_diaria" placeholder="Ex: 50"
                                name="capacidade_diaria" />
                            <font-awesome-icon icon="users" class="text-gray-500" />
                        </label>
                    </div>

                    <div class="flex flex-col">
                        <label for="">
                            Valor <span class="text-red-500">*</span>
                        </label>
                        <label class="input rounded-2xl w-60">
                            <input type="number" placeholder="Ex: 50" v-model="form.valor" name="valor" />
                        </label>
                    </div>
                </div>

                <div class="flex flex-col gap-2 w-full mt-5 ">
                    <span class="text-sm  uppercase font-medium text-gray-500 flex items-center gap-2">
                        <font-awesome-icon icon="info-circle" class="" />
                        Informações adicionais
                    </span>
                    <label for="" class="mt-5">
                        Descrição da rota <span class="text-red-500">*</span>
                    </label>
                    <textarea 
                        class="input rounded-2xl h-24 resize-none pt-2 w-full"
                        placeholder="Descreva os detalhes da rota..." v-model="form.descricao"
                        name="descricao"></textarea>
                </div>
                <div class="flex justify-start mt-6">
                    <!-- <hr class="my-4 border-gray-500" /> -->
                    <button class="btn bg-amber-500 shadow-none text-white rounded-2xl px-6">
                        Atualizar Rota
                    </button>
                </div>
            </div>
        </div>
    </form>
</template>

<script setup >
import { useForm } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

const props = defineProps({
    rota: Object
})

const form = useForm({
    id : props.rota.id || null,
    nome: props.rota.nome || '',
    saindo_de: props.rota.saindo_de || '',
    indo_para: props.rota.indo_para || '',
    capacidade_diaria: props.rota.capacidade_diaria || '',
    valor: props.rota.valor || '',
    horario_partida: props.rota.horario_partida || '',
    ativo: props.rota.ativo || false,
    descricao: props.rota.descricao || '',
})



function submit(e) {
    e.preventDefault()
    form.post(`/viagens/rotas/${props.rota.id}/edit`, {
        onSuccess: () => {
            Swal.fire({
                icon: 'success',
                title: 'Rota atualizada com sucesso!',
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
                title: 'Erro ao atualizar a rota',
                text: mensagem,
            })
        },
        forceFormData: true
    })
}
</script>