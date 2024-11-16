import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import { createPinia } from 'pinia'
import BackButton from '@/components/BackButton.vue'


const app = createApp(App)

app.use(router)
app.use(createPinia())
app.component('BackButton', BackButton)


app.mount('#app')
