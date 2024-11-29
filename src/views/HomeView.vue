<template>
  <div class="md:flex">
    <div class="p-8 w-full">
      <div class="uppercase tracking-wide text-sm text-primary font-semibold">Faça a Diferença</div>
      <h1 class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
        Doe Agora
      </h1>
      <p class="mt-4 max-w-2xl text-xl text-gray-500">
        Sua doação ajuda a transformar vidas. Cada centavo conta para nossa causa.
      </p>

      <form @submit.prevent="newPayment" class="mt-8 space-y-6">
        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700"
            >Valor da Doação <span class="text-red-600">*</span></label
          >
          <div class="flex flex-wrap gap-4">
            <div
              v-for="(payment, key) in payments"
              :key="key"
               :for="`ingredient${payment.key}`"
              class="flex items-center ps-4 px-2 border border-primary rounded"
            >
              <input type="radio"
                :id="`ingredient${payment.key}`"
                v-model="form.donationAmountType"
                :value="payment.key"
                :name="`ingredient${payment.key}`"
                class="w-5 h-5 accent-primary text-primary hover:border-primary focus:outline-none focus:ring focus:ring-primary"

              />
              <label
                :for="`ingredient${payment.key}`"
                class="w-full py-4 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                {{ payment.value }}
              </label>
            </div>
          </div>
        </div>

        <div v-if="form.donationAmountType == 'personalizado'">
          <label for="amount" class="block text-sm font-medium text-gray-700">Outro Valor <span class="text-red-600">*</span></label>
          <div class="mt-1 relative rounded-md shadow-sm">
            <InputText
              class="w-full hover:border-primary focus:border-primary"
              v-money="money"
              v-model="form.donationAmount"
              name="amount"
              id="amount"
              placeholder="0.00"
              min="1"
              step="0.01"
              required
            />
          </div>
        </div>

        <div>
          <label for="paymentMethod" class="block text-sm font-medium text-gray-700">
            Método de Pagamento <span class="text-red-600">*</span>
          </label>
          <Select
            id="paymentMethod"
            name="paymentMethod"
            v-model="form.paymentMethod"
            :options="paymentMethods"
            required
            optionLabel="name"
            optionKey="value"
            placeholder="Selecione um método"
            class="w-full appearance-none accent-primary text-primary hover:border-primary focus:outline-none focus:ring focus:ring-primary"
          />
        </div>

        <div v-if="form.paymentMethod?.value === 'credit-card'">
          <label for="paymentMethod" class="block text-sm font-medium text-gray-700">
            Frequência
          </label>
          <Select
            id="paymentMethod"
            name="paymentMethod"
            v-model="form.Frequency"
            :options="[
              {value: 'one' ,name: '1 Vez'},
              {value: 'weekly' ,name: 'Semanal'},
              {value: 'monthly' ,name: 'Mensal'},
            ]"
            required
            optionLabel="name"
            optionKey="value"
            placeholder="Selecione um método"
            class="w-full hover:border-primary focus:border-primary active:border-primary accent-pink-300 md:accent-pink-500"
          />
        </div>

        <div>
          <Button
            type="submit"
            :loading="loading"
            :label="continueButtonText"
            icon="pi pi-heart"
            class="w-full button-primary"
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
import { currencyBR } from '../utils/FormatMonetaryValue'

const router = useRouter()

const payments = [
  { value: currencyBR('20'), key: '20' },
  { value: currencyBR('50'), key: '50' },
  { value: currencyBR('100'), key: '100' },
  { value: currencyBR('220'), key: '220' },
  { value: 'Outro', key: 'personalizado' },
]

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
  donationAmountType: '',
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
      donationAmount: form.value.donationAmountType === 'personalizado' ? form.value.donationAmount.replace('R$ ', '').replace('.', '').replace(',', '.') : form.value.donationAmountType,
      browserInfo: navigator.userAgent,
      userIP: userIP,
    })
    router.push({ name: 'payment', params: { code: docRef.id } })
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
