import Vue from 'vue'
import Router from 'vue-router'
import Admin from './views/Admin.vue'
import Login from './components/login.vue'
import store from './store'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Admin',
      component: Admin
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})


router.beforeEach((to, from, next) => {
    if(to.path != '/login') {
        if(store.getters.isLoggedIn) {
            console.log('There is a token, resume. (' + to.path + ')');
            next();
        } else {
            console.log('There is no token, redirect to login. (' + to.path + ')');
            next('login');
        }
    } else {
        console.log('You\'re on the login page');
        next(); // This is where it should have been
    }
    // next(); - This is in the wrong place
});

export default router
