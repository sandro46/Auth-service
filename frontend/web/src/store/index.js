import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import product from './product'
import prod_cat from './prodCat'
import prod_component from './prodComponent'
import prod_section from './prodSection'
import office from './office'
import client from './client'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    product,
    prod_cat,
    prod_component,
    prod_section,
    office,
    client,
  }
})
