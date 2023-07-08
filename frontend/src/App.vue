<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <RegionTable :parentId=0 :levelId=1 hierarchy="adm" />
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import RegionTable from "./components/RegionTable.vue";

export default {
  name: 'App',
  components: {
    // HelloWorld,
    RegionTable
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
body {
  background-color: #0a194d0D!important;
}
</style>
