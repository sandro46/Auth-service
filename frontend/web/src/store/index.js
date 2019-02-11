import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import product from './product'
import prod_cat from './prodCat'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    product,
    prod_cat,
  }
})
