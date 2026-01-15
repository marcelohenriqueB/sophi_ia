<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div class="w-full max-w-md">
            <!-- Card de Login -->
            <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
                <!-- Header -->
                <div class="bg-slate-700 px-8 py-10 text-center">
                    <div class="inline-block p-4 bg-slate-600 rounded-2xl mb-4">
                        <font-awesome-icon icon="ship" class="text-white text-4xl" />
                    </div>
                    <h1 class="text-3xl font-bold text-white">Sophi IA</h1>
                    <p class="text-slate-300 text-sm mt-2">gestão fluvial</p>
                </div>

                <!-- Form -->
                <div class="px-8 py-10">
                    <form @submit.prevent="submit">
                        <!-- Mensagens de Erro -->
                        <div v-if="errors && Object.keys(errors).length > 0" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-2xl">
                            <div class="flex items-center gap-2 text-red-600 text-sm">
                                <font-awesome-icon icon="exclamation-circle" />
                                <span v-for="(error, key) in errors" :key="key">{{ error }}</span>
                            </div>
                        </div>

                        <div class="flex flex-col gap-6">
                            <!-- Email -->
                            <div class="flex flex-col gap-2">
                                <label for="email" class="text-sm font-medium text-gray-700">
                                    Email <span class="text-red-500">*</span>
                                </label>
                                <label class="input rounded-2xl">
                                    <input 
                                        type="email" 
                                        id="email"
                                        v-model="form.email" 
                                        placeholder="seu@email.com" 
                                        required
                                        class="w-full"
                                        autocomplete="email"
                                    />
                                    <font-awesome-icon icon="envelope" class="text-gray-500" />
                                </label>
                            </div>

                            <!-- Senha -->
                            <div class="flex flex-col gap-2">
                                <label for="password" class="text-sm font-medium text-gray-700">
                                    Senha <span class="text-red-500">*</span>
                                </label>
                                <label class="input rounded-2xl">
                                    <input 
                                        :type="showPassword ? 'text' : 'password'" 
                                        id="password"
                                        v-model="form.password" 
                                        placeholder="••••••••" 
                                        required
                                        class="w-full"
                                        autocomplete="current-password"
                                    />
                                    <button 
                                        type="button" 
                                        @click="showPassword = !showPassword"
                                        class="text-gray-500 hover:text-gray-700"
                                    >
                                        <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" />
                                    </button>
                                </label>
                            </div>

                            <!-- Lembrar-me -->
                            <div class="flex items-center justify-between">
                                <label class="flex items-center gap-2 cursor-pointer">
                                    <input 
                                        type="checkbox" 
                                        v-model="form.remember" 
                                        class="checkbox checkbox-sm checkbox-primary rounded"
                                    />
                                    <span class="text-sm text-gray-600">Lembrar-me</span>
                                </label>
                                
                                <a href="#" class="text-sm text-purple-600 hover:text-purple-700 font-medium">
                                    Esqueceu a senha?
                                </a>
                            </div>

                            <!-- Botão de Login -->
                            <button 
                                type="submit" 
                                :disabled="form.processing"
                                class="btn bg-purple-500 hover:bg-purple-600 text-white rounded-2xl w-full shadow-lg"
                                :class="{ 'loading': form.processing }"
                            >
                                <font-awesome-icon v-if="!form.processing" icon="sign-in-alt" />
                                {{ form.processing ? 'Entrando...' : 'Entrar' }}
                            </button>
                        </div>
                    </form>
                </div>

                <!-- Footer -->
                <div class="px-8 py-6 bg-gray-50 border-t border-gray-200 text-center">
                    <p class="text-sm text-gray-600">
                        Não tem uma conta? 
                        <a href="#" class="text-purple-600 hover:text-purple-700 font-medium">Cadastre-se</a>
                    </p>
                </div>
            </div>

            <!-- Copyright -->
            <div class="mt-8 text-center">
                <p class="text-white text-sm opacity-75">
                    © 2024 Sophi IA. Todos os direitos reservados.
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useForm } from '@inertiajs/vue3'

// Definir que esta página não usa layout
defineOptions({
    layout: null
})

// Props para receber erros do backend
const props = defineProps({
    errors: {
        type: Object,
        default: () => ({})
    }
})

// Estado
const showPassword = ref(false)

// Form usando Inertia
const form = useForm({
    email: '',
    password: '',
    remember: false
})

// Submeter o formulário
const submit = () => {
    form.post('/login', {
        
        onFinish: () => {
            // Limpar senha em caso de erro
            if (Object.keys(props.errors).length > 0) {
                form.password = ''
            }
        },
        forceFormData: true
    })
}
</script>

<style scoped>
/* Animações suaves */
/* .input:focus-within {
    ring: 2px solid rgb(168 85 247 / 0.5);
} */

button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}
</style>
