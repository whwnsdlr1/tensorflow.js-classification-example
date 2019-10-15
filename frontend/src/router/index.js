import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index.vue'
import Main from '@/components/Main.vue'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/mnist', component: Main },
    { path: '/imagenet', component: Main },
    { path: '*', component: Index }
  ],
  mode: 'history'
})