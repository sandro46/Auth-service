import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import product from './product'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    product
  }
})
