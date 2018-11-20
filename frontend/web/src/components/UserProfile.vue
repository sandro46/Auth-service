<template>

  <div class="main_wrap">
     <b-row >
        <b-col cols="2">
          <LeftMenu />
        </b-col>
        <b-col md="10">
          <h3>Профиль {{ `${user.name ? user.name : ''}` }}</h3>
          <form class=""  @submit="onSubmit" @reset="onReset">
            <b-row>
              <b-col md='3'>
                  <label class="mr-sm-2" :for='user.name'>Имя пользователя:</label>
                  <b-form-input type="text" v-model='user.name'  ></b-form-input>
              </b-col>
              <b-col md='3'>
                  <label class="mr-sm-2" :for='user.phone'>Телефон:</label>
                  <b-form-input  type="text" v-model='user.phone'  ></b-form-input>
              </b-col>
              <b-col md='3'>
                  <label class="mr-sm-2" :for='user.role_id'>Роль:</label>
                  <b-form-select v-model="user.role_id" :options="user_roles"  />
              </b-col>
              <b-col md='3'>
                  <label class="mr-sm-2" > 123</label>
                  <b-button type="submit" variant="success">Сохранить</b-button>
              </b-col>
            </b-row>
          </form>
        </b-col>
      </b-row>
    </div>


</template>

<script>

import LeftMenu from './LeftMenu.vue'

export default {
  name: 'UserProfile',
  components: {
    LeftMenu
  },
  data () {
    return { }
  },
  mounted: async function() {
    if(!this.user.id){
      let res = await this.$store.dispatch('getUser', this.$route.params.id)
      if(!res) {
        window.alert(this.$store.getters.getErrDescrioption)
      }
      res = await this.$store.dispatch('loadUserRoles')
      if(!res) {
        window.alert(this.$store.getters.getErrDescrioption)
      }
    }
  },
  computed: {
     user() {
       let u = this.$store.getters.getUserById(this.$route.params.id)
       return  u ? u : {}
    },
    user_roles(){
      let r = this.$store.getters.user_roles
      return  r ? r : []
    }
  },
  methods: {
    onSubmit(evt){
      evt.preventDefault();
      console.log(JSON.stringify(this.form));
    },
    onReset(evt){
      evt.preventDefault();
    }
  },
}
</script>
