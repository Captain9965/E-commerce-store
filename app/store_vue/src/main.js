import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'http://52.91.162.34:80'
createApp(App).use(store).use(router, axios).mount('#app')
