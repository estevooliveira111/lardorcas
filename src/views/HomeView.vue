<template>
  <div class="bg-white text-gray-900 font-sans">

    <section class="mb-12 bg-white flex justify-center items-center flex-wrap space-y-4 sm:space-y-0 sm:space-x-4">
      <img src="../assets/logo2.png" class="h-36 w-auto"/>
      <img src="../assets/logo1.png" class="h-24 w-24"/>
    </section>

    <section class="mb-28 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <blockquote class="text-lg sm:text-xl italic mb-3">
          "Ordene-lhes que pratiquem o bem, sejam ricos em boas obras, generosos e prontos a repartir." - 1 Tm 6.18
        </blockquote>
        <p class="text-xl sm:text-2xl mb-8">
          Seja a ponte que leva esperança a quem mais precisa. Sua solidariedade ajuda a transformar histórias.
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5">
          <Card v-for="(plan, key) in plans" :key="key" class="border-[#0076AF] bg-white border-2 rounded-xl p-5 shadow-lg text-center">
            <template #content>
              <!-- <p class="text-lg font-bold">{{ plan.label }}</p> -->
              <p class="text-2xl my-4"><span class="font-black">{{ plan.value }}</span>/mês</p>
              <a
                :href="plan.link"
                target="_blank"
                class="w-full inline-block text-center border-[#0076AF] bg-gradient-to-r from-[#0076AF] to-teal-400 text-white font-bold py-2 px-4 rounded hover:from-[#0076AF] hover:to-[#00D0DE] transition duration-300"
              >
                Contribuir
              </a>
            </template>
          </Card>
        </div>
      </div>
    </section>

    <section class="bg-teal-500 text-white py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-44 text-center lg:text-left">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12 lg:gap-20 justify-items-center items-center">

          <div class="grid grid-cols-2 gap-4 text-center lg:text-left">
            <div>
              <h3 class="text-3xl sm:text-4xl font-black">24</h3>
              <p class="text-lg">Projetos ativos</p>
            </div>
            <div>
              <h3 class="text-3xl sm:text-4xl font-black">+440</h3>
              <p class="text-lg">Crianças & adolescentes</p>
            </div>
            <div>
              <h3 class="text-3xl sm:text-4xl font-black">+340</h3>
              <p class="text-lg">Famílias assistidas</p>
            </div>
            <div>
              <h3 class="text-3xl sm:text-4xl font-black">+300</h3>
              <p class="text-lg">Cestas básicas doadas</p>
            </div>
          </div>

          <div class="flex justify-center lg:justify-start">
            <a
                href="https://drive.google.com/file/d/1xVDMiPEtwZRyQb5VAj5cZ0k9nf2KeHf5/view?usp=drive_link"
                target="_blank" class="mt-8 px-12 py-6 font-bold text-base bg-white text-teal-500 rounded-lg shadow-lg hover:bg-gray-100 hover:text-teal-600 hover:scale-105 transition duration-300 transform">
              Conheça nossos projetos
            </a>
          </div>

          <div class="flex flex-col items-start">
            <a href="https://wa.me/+5531988957154" target="_blank" class="flex items-center space-x-1 hover:bg-white font-bold rounded-md hover:text-primary p-1">
              <i class="pi pi-whatsapp mx-5" style="font-size: 2rem"></i>
              <label class="text-lg underline hover:no-underline">Dúvidas? <br> Entre em contato!</label>
            </a>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { Card } from 'primevue';

const plans = [
  {label: 'Transformar', value: 50, link: 'https://sistema.zixpay.com.br/app/plano/ac3e995d-fae3-4a88-a480-acf1d567ad96/assinar'},
  {label: 'Impulso Inicial', value: 100, link: 'https://sistema.zixpay.com.br/app/plano/96e7b913-6f83-47ec-87fc-cee994ce413a/assinar'},
  {label: 'Líder de Mudança', value: 250, link: 'https://sistema.zixpay.com.br/app/plano/758e038f-9eae-4f6e-a3a2-2362215297ca/assinar'},
  {label: 'Arquiteto da Revolução', value: 500, link: 'https://sistema.zixpay.com.br/app/plano/1e56b122-3451-4e9d-9679-43400d41c516/assinar'},
  {label: 'Legado de Impacto', value: 1000, link: 'https://sistema.zixpay.com.br/app/plano/cae79a21-cd16-4d94-8f0e-c12a615f8dc2/assinar'}
];
</script>
