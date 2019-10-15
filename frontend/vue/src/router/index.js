import Vue from 'vue'
import Router from 'vue-router'
import VueClipboard from 'vue-clipboard2'
import home from '@/components/apps/home'
import faq from '@/components/apps/faq'
import imprint from '@/components/apps/imprint'
import single_connection from '@/components/apps/single_connection'

Vue.use(Router);
Vue.use(VueClipboard);

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
      component: single_connection,
      children: [
        {
          path: ':id',
          name: 'id',
          component: single_connection
        }
      ]
    },
    {
      path: '/faq',
      name: '/faq',
      component: faq
    },
    {
      path: '/imprint',
      name: '/imprint',
      component: imprint
    },
  ]
})
