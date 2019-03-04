<template>

    <b-nav vertical class="">
      <b-nav-item ><router-link to="/user">Пользователи</router-link></b-nav-item>
      <b-nav-item ><router-link to="/product">Продукты</router-link></b-nav-item>
      <b-nav-item ><router-link to="/office">Офисы</router-link></b-nav-item>
      <b-nav-item ><router-link to="/prod-section">Цеха</router-link></b-nav-item>
      <!-- <b-nav-item>Link</b-nav-item>
      <b-nav-item>Another Link</b-nav-item>
      <b-nav-item disabled>Disabled</b-nav-item> -->
    </b-nav>

</template>

<script>
export default {
  name: 'LeftMenu'
}
</script>
