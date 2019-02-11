import Vue from 'vue'
import Router from 'vue-router'
import adminStartpage from './components/adminStartpage.vue'
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
      component: adminStartpage
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/user',
      name: 'User',
      component: () => import(/* webpackChunkName: "about" */ './components/User.vue')
    },
    {
      path: '/user/:id',
      name: 'user_profile',
      component: () => import(/* webpackChunkName: "about" */ './components/UserProfile.vue')
    },
    {
      path: '/product',
      name: 'product',
      component: () => import(/* webpackChunkName: "about" */ './components/Product.vue')
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
