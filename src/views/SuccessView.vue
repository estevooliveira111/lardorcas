<template>
  <div class="bg-white h-screen">

    <div class="mb-12 bg-white flex justify-center items-center flex-wrap space-y-4 sm:space-y-0 sm:space-x-4">
      <img src="../assets/logo2.png" class="h-36 w-auto"/>
      <img src="../assets/logo1.png" class="h-24 w-24"/>
    </div>

    <div class="max-w-md bg-white mx-auto border-2 rounded-xl border-primary shadow-xl overflow-hidden md:max-w-2xl">
      <div class="mt-6 p-6 text-center">
        <CheckCircleIcon class="h-12 w-12 text-green-500 mx-auto" />
        <h2 class="mt-2 text-lg font-medium text-gray-900">Obrigado pela sua doação!</h2>
        <p class="mt-1 text-sm text-gray-500">Sua generosidade faz a diferença.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { CheckCircleIcon } from 'lucide-vue-next'
</script>
