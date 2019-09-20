import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/apps/home'
import single_connection from '@/components/apps/single_connection'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: '/home',
      component: home
    },
    {
      path: '/single_connection',
      name: '/single_connection',
      component: single_connection
    }

  ]
})
