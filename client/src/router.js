import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Auth from './views/Auth.vue';
import Log from './components/Log.vue';
import FavoriteThings from './components/FavoriteThings.vue';
import FavoriteThingDetails from './components/FavoriteThingDetails.vue';
import FavoriteThingForm from './components/FavoriteThingForm.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/auth',
      name: 'auth',
      component: Auth,
    },
    {
      path: '/things',
      name: 'favorite-things',
      component: FavoriteThings,
    },
    {
      path: '/things/create',
      name: 'favorite-thing-form',
      component: FavoriteThingForm,
    },
    {
      path: '/things/:id/edit',
      name: 'favorite-thing-edit',
      component: FavoriteThingForm,
    },
    {
      path: '/things/:id',
      name: 'favorite-thing-detail',
      component: FavoriteThingDetails,
    },
    {
      path: '/logs',
      name: 'audit-logs',
      component: Log,
    },
  ],
});
