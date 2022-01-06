import { createApp } from 'vue'
import { registerSW } from 'virtual:pwa-register'
import VueApexCharts from "vue3-apexcharts"

import App from './App.vue'


const app = createApp(App)
app.use(VueApexCharts)

const updateSW = registerSW({ immediate: true })
app.mount('#app')
