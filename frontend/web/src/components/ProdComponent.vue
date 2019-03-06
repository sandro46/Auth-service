<template>

<div class="main_wrap">

  <b-row >
    <b-col md="12">
      <b-table
         small
         hover
         :items="items"
         :fields="fields"
         :tbody-tr-class="rowClass"
         >


         <template slot="HEAD_actions" slot-scope="data">
           <!-- A custom formatted header cell for field 'name' -->
           <b-button type="submit" @click="openNewDialog" variant="success">+</b-button>
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

         <template slot="row-details" slot-scope="row">
            <b-card>
              <form class=""   @submit="onSubmit" >
                <b-row>
                  <b-col md='8'>
                      <label class="mr-sm-2" :for='modifyConteiner.text'>Название:</label>
                      <b-form-input type="text" v-model='modifyConteiner.text'  ></b-form-input>
                  </b-col>
                  <b-col md='4'>

                  </b-col>
                </b-row >
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
                <b-row >
                  <b-col md='12'>
                    <label class="mr-sm-2" :for='modifyConteiner.value'>&nbsp;</label>
                    <br>
                    <b-button type="submit" v-model="modifyConteiner.value" variant="success">Сохранить</b-button>
                    <label class="mr-sm-2" :for='modifyConteiner.value'>&nbsp;</label>
                    <b-button type="button" v-on:click="closeNewDialog(modifyConteiner.value)" variant="default">Отмена</b-button>
                  </b-col>
                </b-row >
              </form>
            </b-card>
         </template>
       </b-table>
     </b-col>
   </b-row>
  </div>

</template>

<script>

  export default {
    name: 'ProdComponent',
    data () {
      return {
        fields: [
          {key: 'value', label: 'ID'},
          {key: 'text', lable: 'Название'},
          {key: 'actions', label: 'Действия'},
        ],
        modifyConteiner: {},
        filter: null,
      }
    },
    computed: {
      items() {
        // debugger;
        return this.$store.getters.prodComponentList
      },
    },
    mounted: async function () {
      await this.$store.dispatch('loadProdComponentList');
    },
    methods: {
      rowClass(item, type){
        if(!item.value && !item._showDetails) return 'hidden'
      },
      async onSubmit(evt){
        evt.preventDefault();
        if(!this.modifyConteiner.text){
          window.alert('Заполнены не все обязательные параметры')
          return
        }
        // debugger;
        let res = this.modifyConteiner.value ?
                                          await this.$store.dispatch('modifyProdComponent', this.modifyConteiner) :
                                          await this.$store.dispatch('addProdComponent', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }

        this.$store.commit('closeProdComponentDetails')
      },
      async setModifyConteiner(row){
        this.$store.commit('closeProdComponentDetails')
        let obj = {}
        for (let key in row.item) {
          obj[key] = row.item[key];
        }
        this.modifyConteiner = obj
      },
      async delRow(id){
        if(!window.confirm('Вы уверены, что хотите удалить компонент продукта?')) return;
        let res = await this.$store.dispatch('delProdComponent', id)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }
      },
      closeNewDialog(){
        this.modifyConteiner = {}
        this.items[0]['_showDetails'] = false
        this.$store.commit('closeProdComponentDetails')
      },
      async openNewDialog(){
        this.$store.commit('newProdComponentDetails')
        this.modifyConteiner = this.items[0]
      },
    }
  }

</script>
