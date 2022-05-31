<template>
  <Transition name="modal">
    <div v-if="show" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header d-flex align-content-between">
            <span class="fs-4">Cadastrar</span> <button type="button" @click="$emit('close')" class="btn-close" aria-label="Close"></button>
          </div>
          <hr>

          <div class="modal-body">
            <form id="user-form">
              <div class="row my-2">

                <div class="col-3">
                  <label for="id-input" class="form-label">ID</label>
                  <input v-model="form.id" type="number" name="id" class="form-control no-arrow" id="id-input">
                </div>

                <div class="col">
                  <label for="nome-input" class="form-label">Nome</label>
                  <input v-model="form.nome" name="nome" type="text" class="form-control" id="nome-input">
                </div>

              </div>
              <div class="row my-2">

                <div class="col-3">
                  <label for="idade-input" class="form-label">Idade</label>
                  <input v-model="form.idade" type="number" name="idade" class="form-control" id="idade-input">
                </div>

                <div class="col">
                  <label for="nome-github-input" class="form-label">Github User</label>
                  <input v-model="form.nome_github" name="nome_github" type="text" class="form-control" id="nome-github-input">
                </div>

              </div>
              <div class="row my-2">

                <div class="col-2">
                  <label for="cep-input" class="form-label">CEP</label>
                  <input v-model="form.endereco.cep" v-on:blur="getViacepData()" type="text" name="cep" class="form-control" id="cep-input">
                </div>

                <div class="col-2">
                  <label for="uf-input" class="form-label">Estado</label>
                  <select v-model="form.endereco.uf" class="form-select" id="uf-input" name="uf">
                    <option value="AC">AC</option>
                    <option value="AL">AL</option>
                    <option value="AP">AP</option>
                    <option value="AM">AM</option>
                    <option value="BA">BA</option>
                    <option value="CE">CE</option>
                    <option value="DF">DF</option>
                    <option value="ES">ES</option>
                    <option value="GO">GO</option>
                    <option value="MA">MA</option>
                    <option value="MT">MT</option>
                    <option value="MS">MS</option>
                    <option value="MG">MG</option>
                    <option value="PA">PA</option>
                    <option value="PB">PB</option>
                    <option value="PR">PR</option>
                    <option value="PE">PE</option>
                    <option value="PI">PI</option>
                    <option value="RJ">RJ</option>
                    <option value="RN">RN</option>
                    <option value="RS">RS</option>
                    <option value="RO">RO</option>
                    <option value="RR">RR</option>
                    <option value="SC">SC</option>
                    <option value="SP">SP</option>
                    <option value="SE">SE</option>
                    <option value="TO">TO</option>
                  </select>
                </div>

                <input v-model="form.endereco.codigo_ibge" type="hidden" name="codigo_ibge" class="hidden" id="codigo-ibge-input">

                <div class="col-4">
                  <label for="cidade-input" class="form-label">Cidade</label>
                  <select v-model="form.endereco.cidade" class="form-select" name="cidade" id="cidade-input">
                    <option v-for="cidade in municipios" :key="cidade.id" :value="cidade.nome">{{cidade.nome}}</option>
                  </select>
                </div>

                <div class="col-4">
                  <label for="bairro-input" class="form-label">Bairro</label>
                  <input v-model="form.endereco.bairro" name="bairro" type="text" class="form-control" id="bairro-input">
                </div>

              </div>
              <div class="row my-2">
                <div class="col-5">
                  <label for="rua-input" class="form-label">Rua</label>
                  <input v-model="form.endereco.rua" name="rua" type="text" class="form-control" id="rua-input">
                </div>

                <div class="col-3">
                  <label for="numero-input" class="form-label">Número</label>
                  <input v-model="form.endereco.numero" type="number" name="numero" class="form-control no-arrow" id="numero-input">
                </div>

                <div class="col-4">
                  <label for="complemento-input" class="form-label">Complemento</label>
                  <input v-model="form.endereco.complemento" name="complemento" type="text" class="form-control" id="complemento-input">
                </div>
              </div>
            </form>
          </div>
          <hr>
          <div class="modal-footer d-flex align-end">
            <button type="button" @click="$emit('close')" class="bg-white border Bd-Primary Text-Primary rounded-2 px-4 py-2 me-2">Cancelar</button>
            <button type="button" class="Primary text-white rounded-2 border-0 px-4 py-2" @click="createUser(); $emit('close')">Salvar</button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: "BootstrapModal",
  props: {
    show: Boolean,
    api_url: String
  },
  data(){
      this.axios.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios').then(
        result => {
          this.municipios = result.data
        }
      )
    return{
      form: {
        id: '',
        nome: '',
        idade: '',
        nome_github: '',
        endereco: {
          cep: '',
          uf: '',
          cidade: '',
          bairro: '',
          rua: '',
          numero: '',
          complemento: ''
        },
      },
      municipios: []
    }
  },
  methods: {
    createUser(){
      this.axios.post(this.api_url, this.form).then(
          result => {
            console.log(result.data)
          })
    },
    getViacepData(){
      let validacep = /^[0-9]{8}$/
      let cep = this.form.endereco.cep.replace(/\D/g, '')
      if (cep !== "" && validacep.test(cep)){
        let url = "https://viacep.com.br/ws/"+ cep + "/json/"
          delete this.axios.defaults.headers.common['Access-Control-Allow-Origin']
          this.axios.get(url, ).then(
            result => {
              this.form.endereco.rua = result.data.logradouro
              this.form.endereco.complemento = result.data.complemento
              this.form.endereco.bairro = result.data.bairro
              this.form.endereco.cidade = result.data.localidade
              this.form.endereco.uf = result.data.uf
              this.form.endereco.codigo_ibge = result.data.ibge
            })
      }
    }
  }
}
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 800px;
  margin: 0 auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}
.no-arrow::-webkit-inner-spin-button,
.no-arrow::-webkit-outer-spin-button {
  -webkit-appearance: none;
}

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>