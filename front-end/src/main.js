import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import App from './App.vue'

Vue.use(ElementUI)
Vue.prototype.$axios = axios

new Vue({
  el: '#app',
  render: h => h(App)
})
