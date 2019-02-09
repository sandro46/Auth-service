const config = require('./config.json')
// import axios from 'axios'
const helper = require( './helpers.js').default;
console.log(helper);

const axios = helper.axios()
// Add a response interceptor

var   productPattern = {
                    _showDetails: false,
                    id: '',
                    name: '',
                    code: '',
                    price: '',
                    count: '',
                    measure: '',
                    ball: '',
                    nds: '',
                    sale: '',
                    desc: '',
};


const state = {
  // login: {
  //   token: localStorage.getItem('token'),
  //   refreshToken: localStorage.getItem('refreshToken')
  // },

  productList: [
    productPattern
  ],
  categories: [
    {name: 'Category1', desc: 'Cat1'},
    {name: 'Category2', desc: 'Cat2'},
    {name: 'Category3', desc: 'Cat3'},
  ],
  err: ''
}

const getters = {
  productList(){
    return state.productList
  }
}


const mutations = {
  close(state){
    debugger;
  },
  allProducts(state, payload){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.productList = payload
  },
  delProduct(state, id){
    let idx = state.productList.findIndex((el) => { return el.id == id})
    state.productList.splice(idx,1)
  },
  modifyProduct(state, payload){
    let idx = state.productList.findIndex((el) => { return el.id == payload.id})
    state.productList[idx] = payload
  },
  addProduct(state, payload){
    state.productList = state.productList.map((i) => { i['_showDetails'] = false; return i; })
  },
  closeProductDetails(state){
    // debugger;
    let obj = {}
    if(state.productList[0]){
      if(state.productList[0]['id'] == ''){
        for (let key in state.productList[0]) {
          obj[key] = '';
        }
        state.productList[0] = obj;
      }
    }
    state.productList = state.productList.map((i) => { i['_showDetails'] = false; return i; })
  },
  newProductDetails(state){
    if(state.productList[0]){
      if( state.productList[0]['id'] == ''){
        state.productList[0]['_showDetails'] = true;
        return;
      }
    }

    let obj = {}
    for (let key in state.productList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.productList.unshift(obj)

  },
}

const actions = {
  async delProduct({state, commit, rootState}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.delete(`product/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delProduct', id)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async loadProductList({state, commit, rootState}){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.get('product/').catch(helper.errHandler);
    if(!res.err) {
      // debugger;
      commit('allProducts', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async modifyProduct({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.put('product/', payload).catch(helper.errHandler);
    if(!res.err) {
      commit('modifyProduct', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async addProduct({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('product/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.id= res.data.id
      commit('addProduct', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
