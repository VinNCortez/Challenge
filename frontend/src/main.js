import App from './App.vue'
import * as Vue from "vue"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "bootstrap-icons/font/bootstrap-icons.css"
import axios from "axios"
import VueAxios from "vue-axios"

const app = Vue.createApp(App)
app.use(VueAxios, axios).mount('#app')
