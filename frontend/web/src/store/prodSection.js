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

//Вызываются commit`ом
const mutations = {
  allProdSect(state, payload){
    payload = payload.map((i) => { i['_showDetails'] = false; return i; })
    state.prodSectList = payload
  },
  closeProdSectDetails(state){
    let obj = {}
    if(state.prodSectList[0]){
      if(state.prodSectList[0]['id'] == ''){
        for (let key in state.prodSectList[0]) {
          obj[key] = '';
        }
        state.prodSectList[0] = obj;
      }
    }
    state.prodSectList = state.prodSectList.map((i) => { i['_showDetails'] = false; return i; })
  },
  newProdSectDetails(state){
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
  modifyProdSect(state, payload){
    let idx = state.prodSectList.findIndex((el) => { return el.id == payload.id})
    state.prodSectList[idx] = payload
  },
  addProdSect(state, payload){
    state.prodSectList = state.prodSectList.map((i) => { i['_showDetails'] = false; return i; })
  },
  delProdSect(state, id){
    let idx = state.prodSectList.findIndex((el) => { return el.id == id})
    state.prodSectList.splice(idx,1)
  },
}

//Вызываются dispatch`ем
const actions = {
  async loadProdSectList({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.get('prod_section/').catch(helper.errHandler);
    if(!res.err) {
      commit('allProdSect', res.data)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async modifyProdSect({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.put('prod_section/', payload).catch(helper.errHandler);
    if(!res.err) {
      let officeIdx = rootState.office.officeList.findIndex(e => {return e.value == payload.office_id})
      payload.office = rootState.office.officeList[officeIdx]['text']
      commit('modifyProdSect', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async addProdSect({state, commit, rootState}, payload){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    let res = await axios.post('prod_section/', payload).catch(helper.errHandler);
    if(!res.err) {
      payload.value = res.data.value
      let officeIdx = rootState.office.officeList.findIndex(e => {return e.value == payload.office_id})
      payload.office = rootState.office.officeList[officeIdx]['text']
      commit('addProdSect', payload)
      return true;
    }
    return await helper.retHandler(res, commit);
  },
  async delProdSect({state, commit, rootState}, id){
    axios.defaults.headers.common['Authorization'] = "Bearer "+rootState.user.login.token;
    const res = await axios.delete(`prod_section/${id}`).catch(helper.errHandler);
    if(!res.err) {
      commit('delProdSect', id)
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
