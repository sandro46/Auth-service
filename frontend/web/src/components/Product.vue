<template>

  <div class="main_wrap">
     <b-row >
        <b-col cols="2">
          <LeftMenu />
        </b-col>
        <b-col md="10">
          <h3>Продукты</h3>
          <b-row >
            <b-col>
              <b-table
                 small
                 hover
                 :items="items"
                 :fields="fields">

                 <template slot="HEAD_actions" slot-scope="data">
                   <!-- A custom formatted header cell for field 'name' -->
                   <b-button-group>
                     <b-button size="sm" type="submit" @click="openNewDialog" variant="success">+Продукт</b-button>
                     <b-button size="sm" type="submit" @click="showModalProdCat=true" variant="success">Категории</b-button>
                     <b-button size="sm" type="submit" @click="showModalProdComponent=true" variant="success">Компоненты</b-button>
                   </b-button-group>
                 </template>

                 <template slot="row-details" slot-scope="row">
                  <b-card>
                    <form class=""   @submit="onSubmit" >
                      <b-row>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.name'>Название:</label>
                            <b-form-input type="text" v-model='modifyConteiner.name'  ></b-form-input>
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.code'>Артикул:</label>
                            <b-form-input  type="text" v-model='modifyConteiner.code'  ></b-form-input>
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.price'>Цена:</label>
                            <b-form-input type="text" v-model="modifyConteiner.price"   />
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.nds'>НДС:</label>
                            <b-form-input type="text" v-model="modifyConteiner.nds"   />
                        </b-col>
                      </b-row>
                      <b-row>
                        <b-col md='2'>
                            <label class="mr-sm-2" :for='modifyConteiner.count'>Кол-во:</label>
                            <b-form-input type="text" v-model='modifyConteiner.count'  ></b-form-input>
                        </b-col>
                        <b-col md='2'>
                            <label class="mr-sm-2" :for='modifyConteiner.measure'>Ед. измерения:</label>
                            <b-form-input type="text" v-model='modifyConteiner.measure'  ></b-form-input>
                        </b-col>
                        <b-col md='2'>
                            <label class="mr-sm-2" :for='modifyConteiner.ball'>Баллы:</label>
                            <b-form-input type="text" v-model='modifyConteiner.ball'  ></b-form-input>
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.category'>Категория:</label>
                            <b-form-select v-model='modifyConteiner.cat' :options="cat_s" class="mb-1" />
                        </b-col>
                        <b-col md='3'>
                            <label class="mr-sm-2" :for='modifyConteiner.sale'>&nbsp;</label>
                            <br>
                            <b-form-checkbox id="checkbox1"
                               v-model="modifyConteiner.sale"
                               value='Y'
                               unchecked-value="N">
                               Действует скидка
                            </b-form-checkbox>
                        </b-col>
                      </b-row>
                      <b-row>
                        <b-col>
                          <b-form-group label="Компоненты, входящие в состав: ">
                            <b-form-checkbox
                              v-for="option in prod_components"
                              v-model="modifyConteiner.components_list"
                              :key="option.value"
                              :value="option.value"
                              name="flavour4"
                              inline
                            >
                              {{ option.text }}
                            </b-form-checkbox>
                          </b-form-group>
                        </b-col>
                      </b-row>
                      <b-row>
                        <b-col md='12'>
                          <label class="mr-sm-2" :for='modifyConteiner.desc'>Описание:</label>
                          <b-form-textarea id="textarea1"
                                           v-model="modifyConteiner.desc"
                                           :rows="3"
                                           :max-rows="6">
                          </b-form-textarea>
                        </b-col>
                      </b-row>

                      <b-row>
                        <b-col md='12'>
                            <label class="mr-sm-2" :for='modifyConteiner.id'>&nbsp;</label>
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
          </b-row >
        </b-col>
      </b-row>

      <b-modal v-model="showModalProdCat"
         title="Категории продукта"
         size="lg">
         <b-container fluid>
           <prodCat />
         </b-container>
        <div slot="modal-footer" class="w-100">
            <b-btn size="sm" class="float-right" variant="primary" @click="showModalProdCat=false">
              Закрыть
            </b-btn>
        </div>
      </b-modal>

      <b-modal v-model="showModalProdComponent"
         title="Компоненты"
         size="lg"
         no-close-on-backdrop
         >
         <b-container fluid>
           <ProdComponent />
           <!-- <Test /> -->
         </b-container>
        <div slot="modal-footer" class="w-100">
            <b-btn size="sm" class="float-right" variant="primary" @click="showModalProdComponent=false">
              Закрыть
            </b-btn>
        </div>
      </b-modal>


  </div>

</template>

<script>

  import LeftMenu from './LeftMenu.vue'
  import ProdCat from './ProdCat.vue'
  import ProdComponent from './ProdComponent.vue'
  import Test from './Test.vue'

  export default {
    name: 'Product',
    components: {
      LeftMenu,
      ProdCat,
      ProdComponent,
      Test,
    },
    data () {
      return {
        prod_components_checked: [],
        fields: [
          {key: 'name', label: 'Имя'},
          {key: 'code', lable: 'Code'},
          {key: 'price', lable: 'Цена'} ,
          {key: 'actions', label: 'Действия'}
        ],
        modifyConteiner: {},
        showModalProdCat: false,
        showModalProdComponent: false,
      }
    },
    computed: {
      items() { return this.$store.getters.productList },
      cat_s() { return this.$store.getters.prodCatList },
      prod_components() { return this.$store.getters.prodComponentList },
    },
    mounted: async function () {
      await this.$store.dispatch('loadProductList');
      await this.$store.dispatch('getAllProdCats');
    },
    methods: {
      async delRow(id){
        if(!window.confirm('Вы уверены, что хотите удалить продукт?')) return;
        let res = await this.$store.dispatch('delProduct', id)
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

        let res = this.modifyConteiner.id ?
                                          await this.$store.dispatch('modifyProduct', this.modifyConteiner) :
                                          await this.$store.dispatch('addProduct', this.modifyConteiner)
        if(!res) {
          window.alert(this.$store.getters.getErrDescrioption)
          return
        }

        this.$store.commit('closeProductDetails')
      },
      setModifyConteiner(row){
        this.$store.commit('closeProductDetails')
        let obj = {}
        for (let key in row.item) {
          obj[key] = key.indexOf('_list') === -1 && row.item[key] ? String(row.item[key]) : row.item[key];
          // debugger;
          // obj[key] = obj[key] ? obj[key] : ''
        }
        this.modifyConteiner = obj
      },
      closeNewDialog(id){

        this.modifyConteiner = {}
        this.items[0]['_showDetails'] = false
        this.$store.commit('closeProductDetails')
      },
      openNewDialog(){
        // this.$store.commit('closeProductDetails')
        this.$store.commit('newProductDetails')
        this.modifyConteiner = this.items[0]

      }
    }
  }

</script>
