<template>
  <div class="p-5">
    <h1 class="text-3xl font-bold mb-2 text-start">Faça Sua Doação via Cartão de Crédito</h1>
    <h2 class="text-xl font-medium mb-6 text-start text-gray-600">
      Sua doação ajuda a transformar vidas. Contribua para um futuro melhor.
    </h2>

    <div v-if="loading" class="flex justify-center items-center h-64">
      <i class="pi pi-spin pi-spinner text-4xl"></i>
    </div>

    <form v-if="!loading && payment" @submit.prevent="processarPagamento" class="space-y-4">
      <div class="form-group">
        <label for="nome" class="block text-sm font-medium text-gray-700">Nome no Cartão <span class="text-red-600">*</span></label>
        <InputText
          id="nome"
          v-model="form.name"
          required
          placeholder="Nome no Cartão"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-700">E-mail <span class="text-red-600">*</span></label>
        <InputText
          id="email"
          v-model="form.email"
          type="email"
          required
          placeholder="E-mail"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <div class="form-group">
        <label for="cardNumber" class="block text-sm font-medium text-gray-700">Número do Cartão <span class="text-red-600">*</span></label>
        <InputText
          id="cardNumber"
          v-mask="'#### #### #### ####'"
          v-model="form.cardNumber"
          required
          placeholder="Número do Cartão"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <div class="form-group">
        <label for="expirationDate" class="block text-sm font-medium text-gray-700">Data de Expiração <span class="text-red-600">*</span></label>
        <InputText
          id="expirationDate"
          v-mask="'##/##'"
          v-model="form.expirationDate"
          required
          placeholder="MM/AA"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <div class="form-group">
        <label for="cvv" class="block text-sm font-medium text-gray-700">CVV <span class="text-red-600">*</span></label>
        <InputText
          id="cvv"
          v-mask="'###'"
          v-model="form.cvv"
          required
          placeholder="CVV"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <Button
        label="Processar Pagamento"
        type="submit"
        :loading="loading"
        icon="pi pi-credit-card"
        class="w-full button-primary"
      />
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { InputText, Button, useToast } from 'primevue'

const loading = ref(false)
const form = ref({
  name: '',
  email: '',
  cardNumber: '',
  expirationDate: '',
  cvv: ''
})
const payment = ref({
  donationAmount: 100
})
const toast = useToast()

const processarPagamento = async () => {
  loading.value = true


  try {
    const { data } = await axios.post(`${import.meta.env.VITE_EXTERNAL_API}process-payment`, {
    // form.,
    amount: payment.value.donationAmount,
    cardNumber: form.value.cardNumber.replace(/\s/g, ''),
  })

    toast.add({
      severity: 'success',
      summary: 'Pagamento Realizado com Sucesso',
      detail: `Pagamento de R$ ${payment.value.donationAmount / 100} confirmado!`,
      life: 5000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Erro ao Processar Pagamento',
      detail: error.response?.data?.message || 'Ocorreu um erro ao tentar processar o pagamento.',
      life: 5000
    })
  } finally {
    loading.value = false
  }
}
</script>
