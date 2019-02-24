<template>
  <div id="app">
    <div v-if="isUserLoggedIn" class="navbar-wrap">
      <b-navbar toggleable type="light" variant="light">
          <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
          <b-navbar-brand>Admin Tools</b-navbar-brand>
          <b-collapse is-nav id="nav_text_collapse">
              <b-navbar-nav>
                <b-nav-item href="#"><router-link to="/">Startpage</router-link></b-nav-item>
                <!-- <b-nav-item href="#"><router-link to="/">Результаты</router-link></b-nav-item> -->
                <!-- <b-nav-item href="#"><router-link to="/task-manager">Протокол работы</router-link></b-nav-item> -->
                  <!-- <b-nav-text>Navbar text</b-nav-text> -->
              </b-navbar-nav>
          </b-collapse>
          <b-navbar-nav class="ml-auto">
            <b-nav-item href="#" v-on:click="logout">Выйти</b-nav-item>
          </b-navbar-nav>
      </b-navbar>
    </div>
    <b-container class="app-row" fluid>
      <transition  name="fade" mode="out-in">
        <router-view/>
      </transition>
    </b-container>
  </div>
</template>

<script>
  export default {
    name: 'App',
    computed: {
        isUserLoggedIn() { return this.$store.getters.isLoggedIn }
    },
    methods:{
      async logout(){
        let result = await this.$store.dispatch('logout')
        if(result){
          this.$router.push('/login')
        }else{
          window.alert(this.$store.getters.getErrDescrioption)
        }
      }
    }
  }
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
.navbar-wrap{
  margin-bottom: 10px;
}
.hidden{
  display: none;
}
</style>
