const config = require('./config.json')
// import axios from 'axios'
const helper = require( './helpers.js').default;
console.log(helper);

const axios = helper.axios()
// Add a response interceptor

const state = {
  prodSectList: [
    {
      'name': '',
      'office_id': '',
      '_showDetails': false
    }
  ]
}
const getters = {
  prodSectList(){
    return state.prodSectList
  }
}

const mutations = {
  allProdSect(){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.prodSectList = payload
  },
  newProdSectDetails(){
    if(state.prodSectList[0]){
      if( state.prodSectList[0]['id'] == ''){
        state.prodSectList[0]['_showDetails'] = true;
        return;
      }
    }

    let obj = {}
    for (let key in state.prodSectList[0]) {
      obj[key] = '';
    }
    obj['_showDetails'] = true;
    state.prodSectList.unshift(obj)
  },
  addProdSect(state, payload){
    state.officeList = state.officeList.map((i) => { i['_showDetails'] = false; return i; })
  },
} //Вызываются commit`ом

const actions = {
  async loadProdSectList({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.get('prod_section/').catch(helper.errHandler);
    if(!res.err) {
      commit('allProdSect', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  }
  async addProdSect({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('prod_section/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.value= res.data.value
      commit('addProdSect', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  }
} //Вызываются dispatch`ем

export default {
  state,
  getters,
  actions,
  mutations
}
