<template>
  <nav class="navbar navbar-background-color">
    <div class="container-fluid">
      <a class="navbar-brand align-top">
        <i class="bi bi-menu-button-wide text-white me-4"></i>
        <img width="80" class="img-fluid" alt="logo_roit.svg" src="../assets/logo_roit.svg">
      </a>
      <form class="d-flex" role="search">
        <div class="input-group">
          <i class="bi bi-search input-group-text text-white Secondary-Dark border-0"></i>
          <input class="form-control me-2 Secondary-Dark border-0 text-white" type="search" placeholder="Busca" aria-label="Busca">
        </div>
      </form>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar"
}
</script>

<style scoped>
.navbar-background-color{
  background-image: linear-gradient(to right, #02202c , #165171);
}
</style>