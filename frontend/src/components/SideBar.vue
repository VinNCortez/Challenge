<template>
  <nav class="nav flex-column align-self-stretch">
    <a class="nav-link active" aria-current="page" href="#"><i class="bi bi-bar-chart-line Text-Secondary"></i></a>
    <a class="nav-link" href="#"><i class="bi bi-building Text-Secondary"></i></a>
    <a class="nav-link" href="#"><i class="bi bi-pencil-square Text-Secondary"></i></a>
    <a class="nav-link" href="#"><i class="bi bi-clipboard-data Text-Secondary"></i></a>
  </nav>
</template>

<script>
export default {
  name: "SideBar"
}
</script>

<style scoped>
.active i{
  color: #E2B87A !important;
}
</style>