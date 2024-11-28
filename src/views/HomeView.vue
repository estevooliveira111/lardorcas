<template>
  <div class="md:flex">
    <div class="p-8 w-full">
      <div class="uppercase tracking-wide text-sm text-primary font-semibold">Faça a diferença</div>
      <h1 class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
        Doe Agora
      </h1>
      <p class="mt-4 max-w-2xl text-xl text-gray-500">
        Sua doação ajuda a transformar vidas. Cada centavo conta para nossa causa.
      </p>

      <form @submit.prevent="newPayment" class="mt-8 space-y-6">
        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700"
            >Valor da Doação</label
          >
          <div class="mt-1 relative rounded-md shadow-sm">
            <InputText
              class="w-full"
              v-money="money"
              name="amount"
              id="amount"
              v-model="form.donationAmount"
              placeholder="0.00"
              min="1"
              step="0.01"
              required
            />
          </div>
        </div>

        <div>
          <label for="paymentMethod" class="block text-sm font-medium text-gray-700"
            >Método de Pagamento</label
          >
          <Select
            id="paymentMethod"
            name="paymentMethod"
            v-model="form.paymentMethod"
            :options="paymentMethods"
            required
            optionLabel="name"
            optionKey="value"
            placeholder="Selecione um método"
            class="w-full"
          />
        </div>

        <div>
          <Button
            type="submit"
            :loading="loading"
            :label="continueButtonText"
            icon="pi pi-heart"
            class="w-full"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { InputText, Select, Button } from 'primevue'

import { db } from '../firebase'

import { useRouter } from 'vue-router'
import { addDoc, collection } from 'firebase/firestore'
const router = useRouter()
const paymentMethods = [
  { value: 'credit-card', name: 'Cartão de Crédito' },
  { value: 'pix', name: 'PIX' },
]
const money = {
  decimal: ',',
  thousands: '.',
  prefix: 'R$ ',
  precision: 2,
  masked: false,
}

const form = ref({
  donationAmount: 0,
  paymentMethod: '',
})
const loading = ref(false)

const continueButtonText = computed(() => {
  if (!form.value.paymentMethod) return 'Doar Agora'
  return `Continuar com ${form.value.paymentMethod === 'credit-card' ? 'Cartão de Crédito' : 'PIX'}`
})

const newPayment = async () => {
  loading.value = true
  try {
    const ipResponse = await fetch('https://api.ipify.org?format=json')
    const ipData = await ipResponse.json()
    const userIP = ipData.ip

    const paysCollection = collection(db, 'pays')
    const docRef = await addDoc(paysCollection, {
      ...form.value,
      browserInfo: navigator.userAgent,
      userIP: userIP,
    })
    router.push({ name: 'payment', params: { code: docRef.id } })
  } catch (error) {
    console.log(error)
  } finally {
    loading.value = false
  }
}
</script>
