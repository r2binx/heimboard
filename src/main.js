import { createApp } from 'vue'
import { useRegisterSW } from 'virtual:pwa-register/vue'
import App from './App.vue'

const intervalMS = 60 * 60 * 1000

const updateServiceWorker = useRegisterSW({
    onRegistered(r) {
        r && setInterval(() => {
            r.update()
        }, intervalMS)
    }
})

const app = createApp(App)
app.mount('#app')
