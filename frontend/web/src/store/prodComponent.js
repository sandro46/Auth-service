const config = require('./config.json')
const helper = require( './helpers.js').default;
console.log(helper);

const axios = helper.axios()

var   prodComponentPattern = {
                    _showDetails: false,
                    value: '',
                    text: '',
};

const state = {
  prodComponentList: [
    prodComponentPattern
  ],
  err: ''
}


const getters = {
  prodComponentList(state){
    return state.prodComponentList
  }
}

const mutations = {
  setProdComponentList(state, payload){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.prodComponentList = payload
  },
  modifyProdComponent(state, payload){
    let idx = state.prodComponentList.findIndex((el) => { return el.value == payload.value})
    state.prodComponentList[idx] = payload
  },
  addProdComponent(state, payload){
    state.prodComponentList = state.prodComponentList.map((i) => { i['_showDetails'] = false; return i; })
  },
  delProdComponent(state, id){
    let idx = state.prodComponentList.findIndex((el) => { return el.value == id})
    state.prodComponentList.splice(idx,1)
  },
  newProdComponentDetails(state){
    if(state.prodComponentList[0]){
      if( state.prodComponentList[0]['value'] == ''){
        state.prodComponentList[0]['_showDetails'] = true;
        return;
      }
    }

    let obj = {}
    for (let key in state.prodComponentList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.prodComponentList.unshift(obj)
  },
  closeProdComponentDetails(state){
    let obj = {}
    if(state.prodComponentList[0]){
      if(state.prodComponentList[0]['value'] == ''){
        for (let key in state.prodComponentList[0]) {
          obj[key] = '';
        }
        state.prodComponentList[0] = obj;
      }
    }
    state.prodComponentList = state.prodComponentList.map((i) => { i['_showDetails'] = false; return i; })
  }
}

const actions = {
  async loadProdComponentList({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.get(`prod_component/`).catch(helper.errHandler);
    if(!res.err) {
      commit('setProdComponentList', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async modifyProdComponent({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    // debugger;
    const res = await axios.put('prod_component/', payload).catch(helper.errHandler);
    if(!res.err) {
      commit('modifyProdComponent', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async delProdComponent(state, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.delete(`prod_component/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delProdComponent', id)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async addProdComponent({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('prod_component/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.value= res.data.id
      commit('addProdComponent', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
}

export default {
  state,
  getters,
  actions,
  mutations
}
