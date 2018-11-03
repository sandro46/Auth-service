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
  err: ''
}

const getters = {
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
  }

}

export default {
  state,
  getters,
  actions,
  mutations
}
