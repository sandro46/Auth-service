<template>

  <div class="main_wrap">
     <b-row >
        <b-col cols="2">
          <LeftMenu />
        </b-col>
        <b-col md="10">
          <h3>Пользователи</h3>
          <b-row >
            <b-col>
              <b-table
                 small
                 hover
                 :items="users"
                 :fields="fields">

                  <template slot="HEAD_actions" slot-scope="data">
                    <!-- A custom formatted header cell for field 'name' -->
                    <b-button type="submit" @click="openNewUserDialog" variant="success">+</b-button>
                  </template>

                 <template slot="actions" slot-scope="row">
                   <b-button-group v-if="row.item.id" size="sm">
                      <b-button size="sm" @click="setModifyConteiner(row)" @click.stop="row.toggleDetails" class="mr-2">
                       Изменить
                      </b-button>
                      <b-button size="sm" @click="delRow(row.item.id)"  class="mr-2">
                       Удалить
                      </b-button>
                   </b-button-group>
                 </template>

                 <template slot="row-details" slot-scope="row">
                  <b-card>
                    <form class=""  @submit="onSubmit" @reset="onReset">
                      <b-row>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.name'>Имя пользователя:</label>
                            <b-form-input type="text" v-model='modifyConteiner.name'  ></b-form-input>
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.phone'>Телефон:</label>
                            <b-form-input  type="text" v-model='modifyConteiner.phone'  ></b-form-input>
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.role_id'>Роль:</label>
                            <b-form-select v-model="modifyConteiner.role_id" :options="user_roles"  />
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.id'>&nbsp;</label>
                            <br>
                            <b-button type="submit" v-model="modifyConteiner.id" variant="success">Сохранить</b-button>
                        </b-col>
                      </b-row>
                    </form>
                  </b-card>
                </template>

              </b-table>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </div>


</template>

<script>

import LeftMenu from './LeftMenu.vue'

export default {
  name: 'User',
  components: {
    LeftMenu
  },
  data () {
    return {
      fields: [
        {key: 'name', label: 'Имя'},
        {key: 'phone', lable: 'Телефон'},
        {key: 'role_name', lable: 'Роль'} ,
        {key: 'actions', label: 'Действия'}
      ],
      modifyConteiner: {},
    }
  },
  mounted: async function () {
    await this.$store.dispatch('loadUserList');
    let res = await this.$store.dispatch('loadUserRoles')
    if(!res) {
      window.alert(this.$store.getters.getErrDescrioption)
    }
  },
  computed: {
    users() { return this.$store.getters.userList },
    user_roles(){
      let r = this.$store.getters.user_roles
      return  r ? r : []
    }
  },
  methods: {
    async delRow(id){
      if(!window.confirm('Вы уверены, что хотите удалить пользователя?')) return;
      let res = await this.$store.dispatch('delUser', id)
      if(!res) {
        window.alert(this.$store.getters.getErrDescrioption)
        return
      }
    },
    openNewUserDialog(){
      this.$store.commit('closeDetails')
      this.$store.commit('newUserDetails')
      this.modifyConteiner = this.users[0]
    },
    setModifyConteiner(row){
      this.$store.commit('closeDetails')
      let obj = {}
      for (let key in row.item) {
        obj[key] = row.item[key];
      }
      this.modifyConteiner = obj
    },
    open(id){
      this.$router.push({ path: `/user/${id}` })
    },
    async onSubmit(evt){
      evt.preventDefault();
      if(!this.modifyConteiner.name || !this.modifyConteiner.phone || !this.modifyConteiner.role_id){
        window.alert('Заполнены не все параметры')
        return
      }
      if(this.modifyConteiner.id){
        let res = await this.$store.dispatch('modifyUser', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }
      } else {
        let res = await this.$store.dispatch('addUser', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }
      }
      this.$store.commit('closeDetails')
    },
    onReset(evt){
      evt.preventDefault();
    }
  }
}
</script>
