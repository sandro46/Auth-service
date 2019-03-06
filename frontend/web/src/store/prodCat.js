const config = require('./config.json')
const helper = require( './helpers.js').default;
console.log(helper);

const axios = helper.axios()

var   productCatPattern = {
                    _showDetails: false,
                    id: '',
                    name: '',
};

const state = {
  prodCatList: [
    productCatPattern
  ],
  err: ''
}


const getters = {
  prodCatList(state){
    return state.prodCatList
  }
}

const mutations = {
  setProdCatList(state, payload){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.prodCatList = payload
  },
  addProdCat(state, payload){
    state.prodCatList = state.prodCatList.map((i) => { i['_showDetails'] = false; return i; })
  },
  modifyProdCat(state, payload){
    let idx = state.prodCatList.findIndex((el) => { return el.value == payload.value})
    state.prodCatList[idx] = payload
  },
  closeProdCatDetails(state){
    let obj = {}
    if(state.prodCatList[0]){
      if(state.prodCatList[0]['id'] == ''){
        for (let key in state.prodCatList[0]) {
          obj[key] = '';
        }
        state.prodCatList[0] = obj;
      }
    }
    state.prodCatList = state.prodCatList.map((i) => { i['_showDetails'] = false; return i; })
  },
  delProdCat(state, id){
    let idx = state.prodCatList.findIndex((el) => { return el.id == id})
    state.prodCatList.splice(idx,1)
  },
  newProdCatDetails(state){
    if(state.prodCatList[0]){
      if( state.prodCatList[0]['id'] == ''){
        state.prodCatList[0]['_showDetails'] = true;
        return;
      }
    }

    let obj = {}
    for (let key in state.prodCatList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.prodCatList.unshift(obj)
  }
}

const actions = {
  async getAllProdCats({state, commit, rootState}){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.get(`prod_cat/`).catch(helper.errHandler);
    if(!res.err) {
      commit('setProdCatList', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },

  async modifyProdCat({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    // debugger;
    const res = await axios.put('prod_cat/', payload).catch(helper.errHandler);
    if(!res.err) {
      commit('modifyProdCat', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async addProdCat({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('prod_cat/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.value= res.data.id
      commit('addProdCat', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async delProdCat({state, commit, rootState}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.delete(`prod_cat/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delProdCat', id)
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
