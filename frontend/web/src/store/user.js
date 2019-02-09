const config = require('./config.json')
// import axios from 'axios'
const helper = require( './helpers.js').default;
console.log(helper);

const axios = helper.axios()
// Add a response interceptor


const state = {
  login: {
    token: localStorage.getItem('token'),
    refreshToken: localStorage.getItem('refreshToken')
  },
  userList: [],
  user_roles: [],
  err: ''
}

const getters = {
  getUserById: (state) => (id) => {
    return state.userList.find(function(user) { return user.id == id })
  },
  userList: (state) => {
    return state.userList
  },
  user_roles(state) {
    return state.user_roles
  },
  isLoggedIn(state) {
    return state.login.token ? true : false
  },
  getErrDescrioption(state){
    return state.err
  },
  getToken(state){
    return state.login.token
  }
}

const mutations = {
  addUser(state, data){
    let role = state.user_roles.find(el => { return el.value == data.role_id })
    data.role_name = role.text
    state.userList.unshift(data)
  },
  modifyUser(state, data){
    let idx = state.userList.findIndex((el) => { return el.id == data.id})
    state.userList[idx] = data
  },
  closeUserDetails(state){
    if(!state.userList[0]['id']) state.userList.splice(0,1)
    state.userList = state.userList.map((i) => { i['_showDetails'] = false; return i; })
  },
  newUserDetails(state){
    let obj = {}
    for (let key in state.userList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.userList.unshift(obj)
  },
  pushUser(state, payload){
    let idx = state.userList.indexOf(el => { return el.id == payload.id })
    if(idx === -1) state.userList.push(payload)
    else state.userList[idx] = payload
  },
  delUser(state, id){
    let idx = state.userList.findIndex((el) => { return el.id == id})
    state.userList.splice(idx,1)
  },
  setUserRoles(state, payload){
    state.user_roles = payload
  },
  setUserList(state, payload){
    state.userList = payload
  },
  clearToken(state){
    state.login.token = null
    state.login.refreshToken = null
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  },
  setLoggedIn(state, payload){
    state.login.token = payload.token
    state.login.refreshToken = payload.refresh_token
    localStorage.setItem('token', payload.token)
    localStorage.setItem('refreshToken', payload.refresh_token)
  },
  setErr(state, err){
    state.err = err
  }
}

const actions = {
  async addUser({commit}, data){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.post('user/', data).catch(helper.errHandler);
    if(!res.err) {
      data.id= res.data.id
      commit('addUser', data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async modifyUser({commit}, data){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.put('user/', data).catch(helper.errHandler);
    if(!res.err) {
      commit('modifyUser', data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async getUser({commit}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.get(`user/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('pushUser', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async delUser({commit}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.delete(`user/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delUser', id)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async loadUserRoles({ commit }){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.get('user/roles').catch(helper.errHandler);
    if(!res.err) {
      commit('setUserRoles', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async loadUserList({ commit }){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.get('user/').catch(helper.errHandler);
    if(!res.err) {
      commit('setUserList', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async login_query({ commit }, payload){
    const res = await axios.post('auth/', payload).catch(helper.errHandler);
    if(!res.err) {
      commit('setLoggedIn', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async logout({ state, commit }){
    axios.defaults.headers.common['Authorization'] = "Bearer "+state.login.token;
    const res = await axios.post('auth/logout').catch((err) => { return helper.errHandler(err, state, commit) } ) ;
    if(!res.err) {
      commit('clearToken')
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
