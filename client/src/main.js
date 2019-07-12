import Vue from 'vue';
import axios from 'axios';
import Cookie from 'js-cookie';
import BootstrapVue from 'bootstrap-vue';
import VeeValidate from 'vee-validate';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCircle, faSquare, faPlusCircle } from '@fortawesome/free-solid-svg-icons';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
  FontAwesomeLayersText,
} from '@fortawesome/vue-fontawesome';
import dotenv from 'dotenv';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

dotenv.config();
const baseUrl = process.env.VUE_APP_AXIOS_BASE_URL;

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.baseURL = baseUrl;
axios.defaults.withCredentials = true;

library.add(faCircle, faSquare, faPlusCircle);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);

Vue.use(VeeValidate, {
  errorBagName: 'vErrors',
  events: 'blur',
});
Vue.use(BootstrapVue);
Vue.config.productionTip = false;

const setCurrentUserToStore = (obj) => {
  const token = Cookie.get('jwt_token');

  if (token) {
    obj.dispatch('authenticateUser');
  } else {
    obj.dispatch('logoutUser');
  }
};

setCurrentUserToStore(store);

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
