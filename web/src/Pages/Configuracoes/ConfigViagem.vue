<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Configurações de Viagem</h1>
        <p class="text-gray-600 mt-2">Gerencie descontos e configurações de pagamento</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="salvarConfiguracao" method="post" class="bg-white rounded-lg shadow-md p-6">
        <!-- Seção de Descontos -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-6 pb-3 border-b-2 border-gray-200">
            Descontos (%)
          </h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Desconto PCD -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Desconto PCD (%)
              </label>
              <input
                v-model.number="formData.desconto_pcd"
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="desconto_pcd"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.00"
              />
              <p class="text-xs text-gray-500 mt-1">Desconto para Pessoas com Deficiência</p>
            </div>

            <!-- Desconto Idoso -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Desconto Idoso (%)
              </label>
              <input
                v-model.number="formData.desconto_idoso"
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="desconto_idoso"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.00"
              />
              <p class="text-xs text-gray-500 mt-1">Desconto para Idosos</p>
            </div>

            <!-- Desconto Criança 0-4 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Desconto Criança 0-4 anos (%)
              </label>
              <input
                v-model.number="formData.desconto_crianca_0_4"
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="desconto_crianca_0_4"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.00"
              />
            </div>

            <!-- Desconto Criança 5-7 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Desconto Criança 5-7 anos (%)
              </label>
              <input
                v-model.number="formData.desconto_crianca_5_7"
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="desconto_crianca_5_7"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.00"
              />
            </div>

            <!-- Desconto Criança 8-10 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Desconto Criança 8-10 anos (%)
              </label>
              <input
                v-model.number="formData.desconto_crianca_8_10"
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="desconto_crianca_8_10"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.00"
              />
            </div>

            <!-- Desconto Acima 11 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Desconto Acima de 11 anos (%)
              </label>
              <input
                v-model.number="formData.desconto_acima_11"
                type="number"
                step="0.01"
                min="0"
                max="100"
                name="desconto_acima_11"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0.00"
              />
            </div>
          </div>
        </div>

        <!-- Seção de Integrações -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-6 pb-3 border-b-2 border-gray-200">
            Integrações
          </h2>

          <div class="grid grid-cols-1 gap-6">
            <!-- Token Asaas -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Token Asaas API
              </label>
              <input
                v-model="formData.token_asaas"
                type="password"
                name="token_asaas"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Cole seu token Asaas aqui"
              />
              <p class="text-xs text-gray-500 mt-1">
                Token para integração com o Asaas (Processamento de pagamentos PIX)
              </p>
            </div>

            <!-- Token Scale4 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Token Scale4
              </label>
              <input
                v-model="formData.token_scale4"
                type="password"
                name="token_scale4"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Cole seu token Scale4 aqui"
              />
              <p class="text-xs text-gray-500 mt-1">
                Token para integração com Scale4 (opcional)
              </p>
            </div>
          </div>
        </div>

        <!-- Seção de Token Admin (JWT) -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-6 pb-3 border-b-2 border-gray-200">
            Token Admin (JWT) - válido por 5 anos
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Token atual
              </label>
              <div class="flex gap-2">
                <input
                  :value="adminToken"
                  readonly
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-700"
                  placeholder="Nenhum token gerado ainda"
                />
                <button type="button" @click="copiarToken" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg">
                  Copiar
                </button>
              </div>
              <p class="text-xs text-gray-500 mt-1">Expira em: {{ adminTokenExpiraEm || '—' }}</p>
            </div>

            <div class="flex md:justify-end">
              <button type="button" @click="gerarTokenAdmin" class="px-6 bg-purple-500 hover:bg-purple-600 text-white font-medium py-2 rounded-lg transition">
                Gerar/Regerar Token (5 anos)
              </button>
            </div>
          </div>
        </div>

        <!-- Botões -->
        <div class="flex gap-3 pt-6 border-t border-gray-200">
          <button
            type="submit"
            :disabled="salvando"
            class="flex-1 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium py-2 px-4 rounded-lg transition"
          >
            <span v-if="!salvando">Salvar Configurações</span>
            <span v-else>Salvando...</span>
          </button>

          <button
            type="button"
            @click="resetarFormulario"
            class="px-6 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 rounded-lg transition"
          >
            Cancelar
          </button>
        </div>
      </form>

    
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { router } from '@inertiajs/vue3'
import Swal from 'sweetalert2'

interface ConfigViagemData {
  desconto_pcd: number
  desconto_idoso: number
  desconto_crianca_0_4: number
  desconto_crianca_5_7: number
  desconto_crianca_8_10: number
  desconto_acima_11: number
  token_asaas: string
  token_scale4: string
}

interface Props {
  config: ConfigViagemData
  mensagem?: string
}

const props = defineProps<Props>()

const salvando = ref(false)
const mensagem = ref({ texto: props.mensagem || '', tipo: props.mensagem ? 'sucesso' : '' })

const formData = ref<ConfigViagemData>({
  desconto_pcd: props.config?.desconto_pcd || 0,
  desconto_idoso: props.config?.desconto_idoso || 0,
  desconto_crianca_0_4: props.config?.desconto_crianca_0_4 || 0,
  desconto_crianca_5_7: props.config?.desconto_crianca_5_7 || 0,
  desconto_crianca_8_10: props.config?.desconto_crianca_8_10 || 0,
  desconto_acima_11: props.config?.desconto_acima_11 || 0,
  token_asaas: props.config?.token_asaas || '',
  token_scale4: props.config?.token_scale4 || ''
})

// Admin token state
const adminToken = ref(props.config?.admin_jwt_token || '')
const adminTokenExpiraEm = ref(props.config?.admin_jwt_expira_em || '')

// Esconder mensagem após 3 segundos
if (props.mensagem) {
  setTimeout(() => {
    mensagem.value = { texto: '', tipo: '' }
  }, 3000)
}

const salvarConfiguracao = () => {
  salvando.value = true
  router.post('/viagens/config-viagem/', formData.value, {
    preserveScroll: true,
    forceFormData: true,
    onSuccess: () => {
      // Esconder mensagem após 3 segundos
      Swal.fire({
        position: 'center',
        icon: 'success',
        title: 'Configurações salvas com sucesso!',
        showConfirmButton: false,
        timer: 2000,
        toast: true
      })
    },

    onFinish: () => {
      salvando.value = false
    }
  })
}

const resetarFormulario = () => {
  formData.value = {
    desconto_pcd: props.config?.desconto_pcd || 0,
    desconto_idoso: props.config?.desconto_idoso || 0,
    desconto_crianca_0_4: props.config?.desconto_crianca_0_4 || 0,
    desconto_crianca_5_7: props.config?.desconto_crianca_5_7 || 0,
    desconto_crianca_8_10: props.config?.desconto_crianca_8_10 || 0,
    desconto_acima_11: props.config?.desconto_acima_11 || 0,
    token_asaas: props.config?.token_asaas || '',
    token_scale4: props.config?.token_scale4 || ''
  }
  mensagem.value = { texto: '', tipo: '' }
}

const copiarToken = async () => {
  if (!adminToken.value) return
  try {
    await navigator.clipboard.writeText(adminToken.value)
    Swal.fire({
      icon: 'success',
      title: 'Token copiado!',
      timer: 1200,
      showConfirmButton: false,
      toast: true,
      position: 'top'
    })
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Não foi possível copiar' })
  }
}

const gerarTokenAdmin = async () => {
  try {
    const resp = await fetch('/users/admin-token', {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    const data = await resp.json()
    if (data.success) {
      adminToken.value = data.token
      adminTokenExpiraEm.value = data.expira_em
      Swal.fire({
        icon: 'success',
        title: 'Token gerado com sucesso!'
      })
    } else {
      throw new Error('Falha ao gerar token')
    }
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Erro ao gerar token' })
  }
}
</script>
