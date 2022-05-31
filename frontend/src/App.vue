<template>
  <nav-bar />
  <div class="d-flex align-items-start" style="height: 800px">
    <side-bar/>
    <div class="m-0 p-4 content w-100 h-100 align-self-stretch">
      <div class="bg-white p-4 rounded-2">
        <content-table/>

        <table-pagination/>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue"
import SideBar from "@/components/SideBar"
import ContentTable from "@/components/ContentTable"
import TablePagination from "@/components/TablePagination"

export default {
  name: 'App',
  components: {
    NavBar,
    SideBar,
    ContentTable,
    TablePagination
  },
  data() {
    this.axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
    return {

    }
  },
}
</script>

<style>
/*@font-face {*/
/*  font-family: Poppins;*/
/*  src: url('https://fonts.google.com/specimen/Poppins');*/
/*}*/

#app {
  font-family: "Open Sans", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.Primary{
  background-color: #E2B87A;
}

.Text-Primary{
  color: #E2B87A !important;
}

.Bd-Primary{
  border: solid 1px #E2B87A !important;
}

.Secondary{
  background-color: #152E3E;
}

.Text-Secondary{
  color: #152E3E;
}

.Secondary-Dark{
  background-color: #02202c !important;
}

button.Bg, .content{
  background-color: #EDEEEF;
}

.Border{
  background-color: #DFE3E6;
}

button, .btn, h1, h2, h3, h4, h5, h6{
  font-family: Poppins, Helvetica, Arial, sans-serif;
  font-weight: bolder !important;
}

table, button{
  font-size: 0.8em !important;
}

</style>
