import { createApp } from 'vue'
import { registerSW } from 'virtual:pwa-register'
import App from './App.vue'

const updateSW = registerSW({ immediate: true })

const app = createApp(App)
app.mount('#app')
