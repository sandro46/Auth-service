<template>

  <div class="main_wrap">

     <b-row >
        <!-- <b-col cols="2">
          <LeftMenu />
        </b-col> -->
        <b-col md="12">
          <h3>Категории продуктов</h3>
          <b-row >
            <b-col>
              <b-table
                 small
                 hover
                 :items="items"
                 :fields="fields">

                 <template slot="HEAD_actions" slot-scope="data">
                   <!-- A custom formatted header cell for field 'name' -->
                   <b-button type="submit" @click="openNewDialog" variant="success">+</b-button>
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

                 <template slot="actions" slot-scope="row">
                   <b-button-group v-if="row.item.value" size="sm">
                      <b-button size="sm" @click="setModifyConteiner(row)" @click.stop="row.toggleDetails" class="mr-2">
                       Изменить
                      </b-button>
                      <b-button size="sm" @click="delRow(row.item.value)"  class="mr-2">
                       Удалить
                      </b-button>
                   </b-button-group>
                 </template>


               </b-table>


            </b-col>
          </b-row >
        </b-col>
     </b-row>

  </div>

</template>

<script>

  import LeftMenu from './LeftMenu.vue'

  export default {
    name: 'ProdCat',
    components: {
      LeftMenu
    },
    data () {
      return {
        fields: [
          {key: 'value', label: 'ID'},
          {key: 'text', lable: 'Название категории'},
          {key: 'actions', label: 'Действия'},
        ],
        modifyConteiner: {},
      }
    },
    computed: {
      items() { return this.$store.getters.prodCatList },
    },
    mounted: async function () {
      await this.$store.dispatch('getAllProdCats');
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
                                          await this.$store.dispatch('modifyProdCat', this.modifyConteiner) :
                                          await this.$store.dispatch('addProdCat', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }

        this.$store.commit('closeProdCatDetails')
      },
      setModifyConteiner(row){
        this.$store.commit('closeProdCatDetails')
        let obj = {}
        for (let key in row.item) {
          obj[key] = row.item[key];
        }
        this.modifyConteiner = obj
      },
      closeNewDialog(){
        this.modifyConteiner = {}
        this.items[0]['_showDetails'] = false
        this.$store.commit('closeProdCatDetails')
      },
      async delRow(id){
        if(!window.confirm('Вы уверены, что хотите удалить категорию продукта?')) return;
        let res = await this.$store.dispatch('delProdCat', id)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }
      },
      openNewDialog(){
        this.$store.commit('newProdCatDetails')
        this.modifyConteiner = this.items[0]
      }
    }
  }

</script>
