<template>

  <div class="main_wrap">
    <b-row >
       <b-col cols="2">
         <LeftMenu />
       </b-col>
       <b-col md="10">
         <h3>Филиалы</h3>
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
                           <label class="mr-sm-2" :for='modifyConteiner.text'>Название:</label>
                           <b-form-input type="text" v-model='modifyConteiner.text'  ></b-form-input>
                         </b-col>
                         <b-col md='8'>
                           <label class="mr-sm-2" :for='modifyConteiner.address'>Адрес:</label>
                           <b-form-input type="text" v-model='modifyConteiner.address'  ></b-form-input>
                         </b-col>
                       </b-row>
                       <b-row>
                        <b-col md='12'>
                          <label class="mr-sm-2" :for='modifyConteiner.desc'>Описание:</label>
                          <b-form-textarea
                                           v-model="modifyConteiner.desc"
                                           :rows="3"
                                           :max-rows="6">
                          </b-form-textarea>
                        </b-col>
                       </b-row>
                       <b-row>
                         <b-col md='12'>
                             <label class="mr-sm-2" :for='modifyConteiner.value'>&nbsp;</label>
                             <br>
                             <b-button type="submit" v-model="modifyConteiner.value" variant="success">Сохранить</b-button>
                             <label class="mr-sm-2" :for='modifyConteiner.value'>&nbsp;</label>
                             <b-button type="button" v-on:click="closeNewDialog(modifyConteiner.value)" variant="default">Отмена</b-button>
                         </b-col>
                       </b-row>
                     </form>
                   </b-card>
                </template>

                <template slot="actions" slot-scope="row">
                  <b-button-group v-if="row.item.value" size="sm">
                     <b-button size="sm" @click="setModifyConteiner(row)" @click.stop="row.toggleDetails" >
                      Изменить
                     </b-button>
                     <b-button size="sm" @click="delRow(row.item.value)">
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
    name: 'Office',
    components: {
      LeftMenu,
    },
    data () {
      return {
        fields: [
          {key: 'value', label: 'ID'},
          {key: 'text', lable: 'Название'},
          {key: 'address', lable: 'Адрес'},
          {key: 'actions', label: 'Действия'},
        ],
        modifyConteiner: {},
        filter: null,
      }
    },
    computed: {
      items() {
        // debugger;
        return this.$store.getters.officeList
      },
    },
    mounted: async function () {
      await this.$store.dispatch('loadOfficeList');
    },
    methods: {
      async onSubmit(evt){
        evt.preventDefault();
        if(!this.modifyConteiner.text){
          window.alert('Заполнены не все обязательные параметры')
          return
        }
        // debugger;
        let res = this.modifyConteiner.value ?
                                          await this.$store.dispatch('modifyOffice', this.modifyConteiner) :
                                          await this.$store.dispatch('addOffice', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }

        this.$store.commit('closeOfficeDetails')
      },
      async setModifyConteiner(row){
        this.$store.commit('closeOfficeDetails')
        let obj = {}
        for (let key in row.item) {
          obj[key] = row.item[key];
        }
        this.modifyConteiner = obj
      },
      async delRow(id){
        if(!window.confirm('Вы уверены, что хотите удалить объект?')) return;
        let res = await this.$store.dispatch('delOffice', id)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }
      },
      closeNewDialog(){
        this.modifyConteiner = {}
        this.items[0]['_showDetails'] = false
        this.$store.commit('closeOfficeDetails')
      },
      async openNewDialog(){
        this.$store.commit('newOfficeDetails')
        this.modifyConteiner = this.items[0]
      },
    }
  }

</script>
