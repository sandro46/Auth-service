<template>
  <div class="login" >

    <b-row class="justify-content-md-center login-row" >
      <b-col cols="12" sm="8" align-self="center">
        <b-form-group id="fieldsetHorizontal"
                      horizontal
                      :label-cols="3"
                      breakpoint="sm"
                      label="Login">
          <b-form-input id="inputHorizontal" v-model='login' ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="12" sm="8" align-self="center">
        <b-form-group id="fieldsetHorizontal"
                      horizontal
                      :label-cols="3"
                      breakpoint="sm"
                      label="Password">
          <b-form-input id="inputHorizontal1" v-model='password' ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="12" sm="6" offset-sm="2" >
        <button v-on:click="login_query" class="btn btn-success form-control">Login</button>
      </b-col>

    </b-row>
  </div>
</template>

<script>
  export default {

    name: 'Login',
    data() {
      return {
        login: 'testuser',
        password: 'testpasswd'
      }
    },
    methods: {
      async login_query(){
        let payload = {login: this.login, password: this.password}
        let result = await this.$store.dispatch('login_query', payload);
        if(result){
          this.$router.go(-1)
        }else{
          window.alert(this.$store.getters.getErrDescrioption)
        }
      }
    }
  }
</script>

<style>
  .login-row { margin-top: 100px; }
</style>
