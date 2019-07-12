import Vue from 'vue';
import Vuex from 'vuex';
import Cookie from 'js-cookie';
import router from '@/router';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isAuthenticated: false,
  },
  mutations: {
    authenticateUser: (state) => {
      state.isAuthenticated = true;
    },
    logoutUser: (state) => {
      state.isAuthenticated = false;
    },
  },
  actions: {
    authenticateUser: ({ commit }, payload) => {
      Cookie.get('jwt_token');
      commit('authenticateUser', payload);
    },
    logoutUser: ({ commit }) => {
      Cookie.remove('jwt_token');
      commit('logoutUser');
      router.push('/');
    },
  },
});
