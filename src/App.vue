<template>
  <div class="bg-white bg-cover bg-center h-screen py-12 px-4 sm:px-6 lg:px-8">

    <div class="justify-center flex">
      <img class="w-1/5 max-w-xs object-contain" src="./assets/Logo para papel Branco.jpg" alt="Imagem">
    </div>

    <div class="max-w-md mx-auto border-2 rounded-xl border-[#524968] shadow-xl overflow-hidden md:max-w-2xl">
      <RouterView />
    </div>
  </div>
  <Toast />
</template>

<script setup>
import { Toast } from 'primevue'
import { onMounted } from 'vue'
import { initFlowbite } from 'flowbite'

onMounted(() => {
  initFlowbite()
})
</script>
