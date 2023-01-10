import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import store from './store'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

axios.defaults.baseURL = 'http://localhost:8000'

createApp(App).use(store).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
