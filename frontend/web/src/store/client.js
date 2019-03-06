const config = require('./config.json')
// import axios from 'axios'
const helper = require( './helpers.js').default;
console.log(helper);

const axios = helper.axios()
// Add a response interceptor

const state = {
  ClientList: [
    {
      'name': '',
      '_showDetails': false
    }
  ]
}
const getters = {
  ClientList(){
    return state.ClientList
  }
}

//Вызываются commit`ом
const mutations = {
  allClient(state, payload){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.ClientList = payload
  },
  closeClientDetails(state){
    let obj = {}
    if(state.ClientList[0]){
      if(state.ClientList[0]['id'] == ''){
        for (let key in state.ClientList[0]) {
          obj[key] = '';
        }
        state.ClientList[0] = obj;
      }
    }
    state.ClientList = state.ClientList.map((i) => { i['_showDetails'] = false; return i; })
  },
  newClientDetails(state){
    if(state.ClientList[0]){
      if( state.ClientList[0]['id'] == ''){
        state.ClientList[0]['_showDetails'] = true;
        return;
      }
    }

    let obj = {}
    for (let key in state.ClientList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.ClientList.unshift(obj)
  },
  modifyClient(state, payload){
    let idx = state.ClientList.findIndex((el) => { return el.id == payload.id})
    state.ClientList[idx] = payload
  },
  addClient(state, payload){
    state.ClientList = state.ClientList.map((i) => { i['_showDetails'] = false; return i; })
  },
  delClient(state, id){
    let idx = state.ClientList.findIndex((el) => { return el.id == id})
    state.ClientList.splice(idx,1)
  },
}

//Вызываются dispatch`ем
const actions = {
  async loadClientList({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.get('client/').catch(helper.errHandler);
    if(!res.err) {
      commit('allClient', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async modifyClient({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.put('client/', payload).catch(helper.errHandler);
    if(!res.err) {
      commit('modifyClient', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async addClient({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('client/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.id = res.data.id
      commit('addClient', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async delClient({state, commit, rootState}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.delete(`client/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delClient', id)
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
