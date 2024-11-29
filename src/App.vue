<template>
  <div class="bg-[#22C0CC] h-screen">

    <div class="justify-center flex">
      <img class="w-1/5 max-w-xs object-contain" src="./assets/image cortada.png" alt="Imagem">
    </div>

    <div class="max-w-md bg-white mx-auto border-2 rounded-xl border-[#524968] shadow-xl overflow-hidden md:max-w-2xl">
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
