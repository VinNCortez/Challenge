<template>
  <div class="d-flex justify-content-between">
    <button @click="showModal = true" type="button" class="button Primary text-white mb-4 border-0 px-4 py-2 rounded-2">
      Cadastrar
    </button>
    <form class="d-flex" role="search" style="height: min-content">
      <div class="input-group">
        <i class="bi bi-search input-group-text bg-white"></i>
        <input class="form-control" type="search" placeholder="Busca" aria-label="Busca">
      </div>
    </form>
  </div>
  <table class="table rounded-4 border fs-small">
    <thead>
      <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>Idade</th>
        <th>GitHub User</th>
        <th>Endereço</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="user in users" :key="user">
        <td>{{user.id}} </td>
        <td>{{user.nome}}</td>
        <td>{{user.idade}} anos</td>
        <td>{{user.nome_github}}</td>
        <td>{{user.endereco.rua}}, {{user.endereco.numero}}, {{user.endereco.bairro}} - {{user.endereco.cidade}}/{{user.endereco.uf}}</td>
        <td class="align-end">
          <i class="bi bi-eye text-black me-3 action" style="font-size: 15px"></i>
          <i @click="deleteUser(user)" class="bi bi-trash red action" style="font-size: 15px; color: red"></i>
        </td>
      </tr>
    </tbody>
  </table>

  <bootstrap-modal :api_url="API_USERS_URL" :show="showModal" @close="showModal = false"/>

</template>

<script>
import BootstrapModal from "@/components/BootstrapModal";

const API_URL = process.env.VUE_APP_API_URL
const API_USERS_URL = API_URL + "/user/"

export default {
  name: "ContentTable",
  components: {
    BootstrapModal
  },
  data(){
    this.axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
    this.axios.get(API_USERS_URL).then(result => {
      this.users = result.data
    })
    return {
      API_URL,
      API_USERS_URL,
      users: null,
      showModal: false
    }
  },
  methods: {
    getUsers(){
      this.axios.get(API_USERS_URL).then(result => {
        this.users = result.data
        console.log(result.data)
      })
    },
    deleteUser(user){
      this.axios.delete(API_USERS_URL+user.id)
    }
  }
}
</script>

<style scoped>
tbody tr:hover, table thead{
  background-color: #F9FAFB;
}

.action{
  cursor: pointer;
}


</style>