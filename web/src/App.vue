<template>
  <BooksTable msg="Welcome to Your Vue.js App"/>
</template>

<script>
import BooksTable from './components/BooksTable.vue'

export default {
  name: 'App',
  components: {
    BooksTable
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
