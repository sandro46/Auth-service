const config = require('./config.json')
const helper = require( './helpers.js').default;

const axios = helper.axios()

const state = {

  officeList: [
    {_showDetails: false}
  ],
  err: ''

}

const getters = {
  officeList(){
    return state.officeList
  }
}


const mutations = {
  allOffices(state, payload){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.officeList = payload
  },
  delOffice(state, id){
    let idx = state.officeList.findIndex((el) => { return el.id == id})
    state.officeList.splice(idx,1)
  },
  modifyOffice(state, payload){
    let idx = state.officeList.findIndex((el) => { return el.id == payload.id})
    state.officeList[idx] = payload
  },
  addOffice(state, payload){
    state.officeList = state.officeList.map((i) => { i['_showDetails'] = false; return i; })
  },
  closeOfficeDetails(state){
    // debugger;
    let obj = {}
    if(state.officeList[0]){
      if(state.officeList[0]['id'] == ''){
        for (let key in state.officeList[0]) {
          obj[key] = '';
        }
        state.officeList[0] = obj;
      }
    }
    state.officeList = state.officeList.map((i) => { i['_showDetails'] = false; return i; })
  },
  newOfficeDetails(state){
    if(state.officeList[0]){
      if( state.officeList[0]['id'] == ''){
        state.officeList[0]['_showDetails'] = true;
        return;
      }
    }

    let obj = {}
    for (let key in state.officeList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.officeList.unshift(obj)

  },
}


const actions = {
  async delOffice({state, commit, rootState}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.delete(`office/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delOffice', id)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async loadOfficeList({state, commit, rootState}){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.get('office/').catch(helper.errHandler);
    if(!res.err) {
      // debugger;
      commit('allOffices', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async modifyOffice({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.put('office/', payload).catch(helper.errHandler);
    if(!res.err) {
      commit('modifyOffice', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async addOffice({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('office/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.value= res.data.value
      commit('addOffice', payload)
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
