import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'
import './../style.css'
import Layout from './Pages/Layouts/Layout.vue'
/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// all icons
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'

const all = [...Object.values(fas), ...Object.values(fab), ...Object.values(far)]

/* add icons to the library */
library.add(...all)

import axios from 'axios'

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
axios.defaults.withCredentials = true

const token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')

if (token) {
  axios.defaults.headers.common['X-CSRFToken'] = token
}

createInertiaApp({
  progress: {
      // The delay after which the progress bar will appear, in milliseconds...
      delay: 250,
      // The color of the progress bar...
      color: '#314158',
      // Whether to include the default NProgress styles...
      includeCSS: true,
      // Whether the NProgress spinner will be shown...
      showSpinner: false,
  },
  
  resolve: (name) => {
    const pages = import.meta.glob('./Pages/**/*.vue', { eager: true })
    let page = pages[`./Pages/${name}.vue`]
    //pagina de login sem layout
    if (name === 'Auth/Login') {
      return page
    }
    page.default.layout = page.default.layout || Layout
    return page
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .component('font-awesome-icon', FontAwesomeIcon)
      .mount(el)
  },
})