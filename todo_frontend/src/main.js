import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import axios from 'axios';
import VueAxios from 'vue-axios';
import auth from './auth';
import wysiwyg from "vue-wysiwyg";

Vue.use(wysiwyg, {});
Vue.use(VueAxios, axios);

auth.checkAuth();
Vue.config.productionTip = false;

router.beforeEach((route, redirect, next) => {
    if ((auth.user.authenticated || route.name === 'Login' || route.name === 'Register')) {
      next();
    } else {
      next('/login');
    }
});

axios.interceptors.request.use(
  config => { 
    const token = auth.getAuthHeader();
    if (token) {
      config.headers.common["Authorization"] = token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app');
