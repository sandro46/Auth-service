import axios from 'axios'

const helper =
      {
        errHandler:  async function (err, state=null, commit=null, request_url = null) {
          let ret_err = ''
          switch (err.request.status) {
            case 401:
              console.log('[ERR] Invalid token');
              console.log('[i] Then send request to refresh token');
              let refresh_token = state.login.refreshToken
              if(refresh_token){
                let axios = this.axios()
                let res = await axios.post('/auth/refresh', { refresh_token }).catch((e) => {
                  console.log(['[ERR] Error refresh token'],e.response.data);
                  return e
                })
                if(res.request.status == 200){
                  console.log('[i] Refresh toke request is successed');
                  commit('setLoggedIn', res.data)
                  console.log('[i] Then we repeat the request that failed to validate the token');
                  err.config.headers['Authorization'] = `Bearer ${state.login.token}`
                    res = await axios({
                      method: err.config.method,
                      url: err.config.url,
                      data: err.config.data ? err.config.data : {},
                      headers: err.config.headers
                    }).catch(function(e) {  console.log(e);  });

                  if(res.status == 200){
                    return true;
                  }
                }
              }
              ret_err = '[ERR] Refresh is failed';
              return {
                err: ret_err,
                status: err.request.status,
                description:  'Вы не авторизованы в системе'
              }
              break;
            case 403:
              ret_err = '[ERR] Bad criditionals for login';
              return {
                err: ret_err,
                status: err.request.status,
                description:  'Неправильное имя пользователя или пароль'
              }
              break;
            case 404:
              ret_err = '[ERR] Not found';
              return {
                err: ret_err,
                status: err.request.status,
                description:  'Запрошен несуществующий ресурс'
              }
              break;
            case 500:
              ret_err = '[ERR] Iternal server error';
              return {
                err: ret_err,
                status: err.request.status,
                description:  'Внутренняя ошибка сервера'
              }
              break;
            default:
              ret_err = '[ERR] Unknown error';
              return {
                err: ret_err,
                status: err.request.status,
                description:  'Неизвестная ошибка'
              }
          }
        },
        retHandler: (res, commit) =>  {
          if(res.err) {
            console.log(res.err);
            if(res.status == 401) commit('clearToken')
            commit('setErr', res.description)
            return false;
          }
          return true
        },
        axios: () => {
          return axios.create({
            baseURL: 'http://localhost:5000/',
            timeout: 5000
          });
        }
      }
export  default helper
