<template>

  <div class="main_wrap">
    <b-row >
       <b-col cols="2">
         <LeftMenu />
       </b-col>
       <b-col md="10">
         <h3>Цеха</h3>
         <b-row>
           <b-col>
             <b-table
                small
                hover
                :items="items"
                :fields="fields">

                <template slot="HEAD_actions" slot-scope="data">
                  <!-- A custom formatted header cell for field 'name' -->
                  <b-button-group>
                    <b-button size="sm" type="submit" @click="openNewDialog" variant="success">+</b-button>
                  </b-button-group>
                </template>

                <template slot="row-details" slot-scope="row">
                   <b-card>
                     <form class=""   @submit="onSubmit" >
                       <b-row>
                         <b-col md='4'>
                           <label class="mr-sm-2" :for='modifyConteiner.name'>Имя:</label>
                           <b-form-input type="text" v-model='modifyConteiner.name'  ></b-form-input>
                         </b-col>
                         <b-col md='4'>
                             <label class="mr-sm-2" :for='modifyConteiner.phone'>Телефон:</label>
                             <b-form-input type="text" v-model='modifyConteiner.phone'  ></b-form-input>
                         </b-col>
                         <b-col md='4'>
                             <label class="mr-sm-2" :for='modifyConteiner.discount'>Скидка:</label>
                             <b-form-input type="number" v-model='modifyConteiner.discount'  ></b-form-input>
                         </b-col>
                       </b-row>
                       <b-row>
                         <b-col md='12'>
                             <label class="mr-sm-2" :for='modifyConteiner.address'>Адрес:</label>
                             <b-form-input type="text" v-model='modifyConteiner.address'  ></b-form-input>
                         </b-col>
                       </b-row>
                       <b-row >
                         <b-col md='12'>
                           <label class="mr-sm-2" :for='modifyConteiner.desc'>Описание:</label>
                           <b-form-textarea id="textarea1"
                                            v-model="modifyConteiner.desc"
                                            :rows="3"
                                            :max-rows="6">
                           </b-form-textarea>
                         </b-col>
                       </b-row >
                       <b-row>
                         <b-col md='12'>
                             <label class="mr-sm-2" :for='modifyConteiner.value'>&nbsp;</label>
                             <br>
                             <b-button type="submit" v-model="modifyConteiner.id" variant="success">Сохранить</b-button>
                             <label class="mr-sm-2" :for='modifyConteiner.id'>&nbsp;</label>
                             <b-button type="button" v-on:click="closeNewDialog(modifyConteiner.id)" variant="default">Отмена</b-button>
                         </b-col>
                       </b-row>
                     </form>
                   </b-card>
                </template>

                <template slot="actions" slot-scope="row">
                  <b-button-group v-if="row.item.id" size="sm">
                     <b-button size="sm" @click="setModifyConteiner(row)" @click.stop="row.toggleDetails" >
                      Изменить
                     </b-button>
                     <b-button size="sm" @click="delRow(row.item.id)">
                      Удалить
                     </b-button>
                  </b-button-group>
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
    name: 'Cliention',
    components: {
      LeftMenu
    },
    data() {
      return {
        fields: [
          {key: 'name', label: 'Имя'},
          {key: 'phone', lable: 'Телефон'},
          {key: 'address', lable: 'Адрес'},
          {key: 'discount', lable: 'Скидка'},
          {key: 'actions', label: 'Действия'}
        ],
        modifyConteiner: {},
      }
    },
    computed: {
      items() { return this.$store.getters.ClientList  },
      officeList() { return this.$store.getters.officeList  }
    },
    mounted: async function () {
      await this.$store.dispatch('loadClientList');
    },
    methods: {
      setModifyConteiner(row){
        this.$store.commit('closeClientDetails')
        let obj = {}
        for (let key in row.item) {
          obj[key] = key.indexOf('_list') === -1 && row.item[key] ? String(row.item[key]) : row.item[key];
        }
        this.modifyConteiner = obj
      },
      openNewDialog(){
        this.$store.commit('newClientDetails')
        this.modifyConteiner = this.items[0]
      },
      closeNewDialog(){
        this.modifyConteiner = {}
        this.items[0]['_showDetails'] = false
        this.$store.commit('closeClientDetails')
      },
      async delRow(id){
        if(!window.confirm('Вы уверены, что хотите удалить объект?')) return;
        let res = await this.$store.dispatch('delClient', id)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }
      },
      async onSubmit(evt){
        evt.preventDefault();
        if(!this.modifyConteiner.name){
          window.alert('Заполнены не все обязательные параметры')
          return
        }
        // debugger;
        let res = this.modifyConteiner.id ?
                                          await this.$store.dispatch('modifyClient', this.modifyConteiner) :
                                          await this.$store.dispatch('addClient', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }

        this.$store.commit('closeClientDetails')
      },
    }
  }

</script>
