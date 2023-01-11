import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import store from './store'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min.js"
import "bootstrap"
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Toaster from '@meforma/vue-toaster'

axios.defaults.baseURL = 'http://localhost:8000'

createApp(App).use(Toaster).use(store).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
