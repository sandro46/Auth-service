<template>

  <div class="main_wrap">
    <!-- <button type="button" v-on:click='groupRows()' name="button">Test</button> -->
     <b-row >
        <b-col cols="2">
          <LeftMenu />
        </b-col>
        <b-col>
          <h3>Admin Home</h3>
        </b-col>
      </b-row>
    </div>



</template>

<script>

import LeftMenu from './LeftMenu.vue'

export default {
  name: 'adminStartpage',
  components: {
    LeftMenu
  },
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
