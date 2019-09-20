// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App'
import Header from './components/header'
import Sidebar from './components/sidebar'
import Footer from './components/footer'
import router from './router'

Vue.config.productionTip = false;

Vue.mixin({
  data: function() {
    return {
      sitename: "Bahnpreise.info",
      updateStats(){
        axios.get(this.apiUrl + '/stats').then(response => {
          console.log(response.data);
          this.stats = response.data;
        });
      },
      //Base API URL
      get apiUrl(){
        return 'https://api.bahnpreise.info'
      },
    }
  }
});

new Vue({
  el: '#header',
  components: { Header },
  template: '<Header/>',
});

new Vue({
  el: '#sidebar',
  components: { Sidebar },
  template: '<Sidebar/>',
});

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});

new Vue({
  el: '#footer',
  router,
  components: { Footer },
  template: '<Footer/>',
});
