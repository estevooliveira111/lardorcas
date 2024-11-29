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
            class="custom-select w-full focus:border-primary w-full active:border-primary hover:border-primary !border-primary"
            placeholder="Selecione um método"
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
import { InputText, Select, Button, useToast } from 'primevue'
import { useRouter } from 'vue-router'
import { addDoc, collection } from 'firebase/firestore'
import { db } from '../firebase'
import { currencyBR } from '../utils/FormatMonetaryValue'

const toast = useToast()
const router = useRouter()

const payments = [
  { value: currencyBR('20'), key: '20' },
  { value: currencyBR('50'), key: '50' },
  { value: currencyBR('100'), key: '100' },
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

const validateForm = () => {
  const donationAmount = form.value.donationAmountType === 'personalizado'
    ? parseFloat(form.value.donationAmount.replace('R$ ', '').replace('.', '').replace(',', '.'))
    : parseFloat(form.value.donationAmountType)

  if (donationAmount < 2) {
    toast.add({
      severity: 'info',
      summary: 'Atenção',
      detail: `O valor mínimo para doação é R$ 2,00`,
      life: 5000,
    })
    return false
  }

  if (!form.value.donationAmountType || !form.value.paymentMethod || (form.value.donationAmountType === 'personalizado' && !form.value.donationAmount)) {
    toast.add({
      severity: 'info',
      summary: 'Atenção',
      detail: `Por favor, preencha todos os campos obrigatórios.`,
      life: 5000,
    })
    return false
  }

  return true
}

const newPayment = async () => {
  if (!validateForm()) return

  loading.value = true
  try {
    const ipResponse = await fetch('https://api.ipify.org?format=json')
    const ipData = await ipResponse.json()
    const userIP = ipData.ip

    const paysCollection = collection(db, 'payments')
    const docRef = await addDoc(paysCollection, {
      ...form.value,
      donationAmount: form.value.donationAmountType === 'personalizado' ? form.value.donationAmount.replace('R$ ', '').replace('.', '').replace(',', '.') : form.value.donationAmountType,
      browserInfo: navigator.userAgent,
      userIP: userIP,
    })

    console.log(form.value.paymentMethod);
    if (form.value.paymentMethod?.value === 'credit-card') {
      return router.push({ name: 'payment_card', params: { code: docRef.id } })
    } else {
      return router.push({ name: 'payment_pix', params: { code: docRef.id } })
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
