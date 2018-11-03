<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <adminStartpage />
  </div>
</template>

<script>
// @ is an alias to /src
import adminStartpage from '@/components/adminStartpage.vue'

export default {
  name: 'Admin',
  components: {
    adminStartpage
  }
}
</script>
