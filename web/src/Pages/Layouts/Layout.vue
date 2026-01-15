<template>
  <div class="min-h-screen bg-gray-50">
    <!-- SIDEBAR FIXA -->
    <aside
      class="fixed top-0 left-0 h-screen w-64 2xl:w-72
             bg-slate-700 border-r border-gray-200
             flex flex-col justify-between p-5 pt-10 z-50"
    >
      <div>
        <!-- LOGO -->
        <div class="text-2xl font-bold mb-8 flex px-2 flex-col gap-3">
          <span class="text-white">
            <span class="px-2 py-2 bg-slate-600 text-white rounded-2xl mr-2">
              <font-awesome-icon icon="ship" />
            </span>
            Sophi IA
          </span>
          <span class="text-sm font-normal text-slate-400">
            gestão fluvial
          </span>
        </div>

        <!-- MENU -->
        <nav>
          <ul class="flex flex-col gap-3">
            <li class="px-3 py-2 rounded-2xl hover:bg-slate-600">
              <a href="/" class="text-white font-semibold">
                <font-awesome-icon icon="dashboard" /> Dashboard
              </a>
            </li>

            <li class=" px-3 py-3 rounded-2xl text-white" :class=" pathname.startsWith('/viagens/rotas') ? 'active' : '' ">
              <a href="/viagens/rotas/list" class=" font-semibold">
                <font-awesome-icon icon="route" /> Rotas
              </a>
            </li>
            <li class="px-3 py-2 rounded-2xl text-white" :class=" pathname.startsWith('/viagens/suites') ? 'active' : '' ">
              <a href="/viagens/suites/list" class=" font-semibold">
                <font-awesome-icon icon="door-open" /> Suítes
              </a>
            </li>

            <li class="px-3 py-2 rounded-2xl text-white" :class=" pathname.startsWith('/viagens/reservas') ? 'active' : '' ">
              <a href="/viagens/reservas/list" class=" font-semibold">
                <font-awesome-icon icon="ticket-simple" /> Reservas
              </a>
            </li>
            <li class="px-3 py-2 rounded-2xl text-white" :class=" pathname.startsWith('/viagens/clientes') ? 'active' : '' ">
              <a href="/viagens/clientes/list" class=" font-semibold">
                <font-awesome-icon icon="users" /> Clientes
              </a>
            </li>

          </ul>
        </nav>
      </div>

      <!-- FOOTER -->
      <div>
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <div
              class="bg-blue-200 text-blue-500 font-bold w-10 h-10
                     rounded-full flex items-center justify-center"
            >
              {{ user.name.charAt(0) }}
            </div>
            <p class="text-white text-sm">{{ user.name }}</p>
          </div>

          <button @click="handleLogout" class="btn btn-ghost bg-slate-600 text-white btn-sm">
            Logout
          </button>
        </div>

        <hr class="my-4 border-gray-500" />
        <p class="text-white text-[10px]">
          © 2024 Sophi IA. All rights reserved.
        </p>
      </div>
    </aside>

    <!-- CONTEÚDO -->
    <main
      class="ml-64 2xl:ml-72 min-h-screen flex flex-col"
    >
      <!-- HEADER -->
      <header
        class="px-10 py-5 border-b border-gray-200
               flex justify-between items-center bg-white sticky top-0 z-40"
      >
        <div>
          <h1 class="text-xl font-semibold">Visão Geral</h1>
          <p class="text-sm text-slate-600">
            Bem-vindo de volta, aqui está o seu resumo.
          </p>
        </div>

        <div class="flex items-center gap-4">
          <label class="input rounded-2xl">
            <font-awesome-icon icon="magnifying-glass" class="mr-2 text-slate-400" />
            <input type="search" placeholder="Buscar reservas" />
          </label>

          <button class="btn btn-ghost bg-slate-200 text-slate-700 btn-sm">
            <font-awesome-icon icon="bell" />
          </button>
        </div>
      </header>

      <!-- PAGE CONTENT -->
      <section class="p-10 flex-1 overflow-y-auto">
        <slot />
      </section>
    </main>
  </div>
</template>


<script setup>
import { computed } from 'vue'
import { usePage, router } from '@inertiajs/vue3'

const page = usePage()
const user = computed(() => page.props.auth.user)
const pathname = window.location.pathname

const handleLogout = () => {
  router.post('/logout')
}

</script>

<style scoped lang="scss">
.active {
  background-color: #475569; /* bg-slate-600 */
  font-weight: 600;
  a{
    color: white !important;
  }
}
</style>