import Vue from 'vue'
import App from './App'
import router from './router'
import VueLodash from 'vue-lodash'
import Toasted from 'vue-toasted'
import Modal from './plugins/modal.js'

Vue.config.productionTip = false

Vue.use(VueLodash)
Vue.use(Toasted)
Vue.use(Modal)

new Vue({
  render: h => h(App),
  router,
  mModal: Modal,
  component: { App }
}).$mount('#app')
