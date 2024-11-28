<template>
  <div class="bg-custom-image bg-cover bg-center h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-xl overflow-hidden md:max-w-2xl">
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
