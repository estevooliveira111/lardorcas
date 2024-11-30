<template>
  <RouterView />
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
