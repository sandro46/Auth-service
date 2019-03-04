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
                         <b-col md='9'>
                           <label class="mr-sm-2" :for='modifyConteiner.text'>Название:</label>
                           <b-form-input type="text" v-model='modifyConteiner.text'  ></b-form-input>
                         </b-col>
                         <b-col md='3'>
                             <label class="mr-sm-2" :for='modifyConteiner.office_id'>Офис:</label>
                             <b-form-select v-model='modifyConteiner.office_id' :options="officeList" class="mb-1" />
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
    name: 'ProdSection',
    components: {
      LeftMenu
    },
    data() {
      return {
        fields: [
          {key: 'text', label: 'Имя'},
          {key: 'office_id', lable: 'Филиал'},
          {key: 'actions', label: 'Действия'}
        ],
        modifyConteiner: {},
      }
    },
    computed: {
      items() { return this.$store.getters.prodSectList  },
      officeList() { return this.$store.getters.officeList  }
    },
    mounted: async function () {
      await this.$store.dispatch('loadProdSectList');
    },
    methods: {
      openNewDialog(){
        this.$store.commit('newProdSectDetails')
        this.modifyConteiner = this.items[0]
      },
      closeNewDialog(){
        this.modifyConteiner = {}
        this.items[0]['_showDetails'] = false
        this.$store.commit('closeProdSect')
      },
      async onSubmit(evt){
        evt.preventDefault();
        if(!this.modifyConteiner.text){
          window.alert('Заполнены не все обязательные параметры')
          return
        }
        // debugger;
        let res = this.modifyConteiner.value ?
                                          await this.$store.dispatch('modifyProdSect', this.modifyConteiner) :
                                          await this.$store.dispatch('addProdSect', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }

        this.$store.commit('closeProdSectDetails')
      },
    }
  }

</script>
