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
        <label for="nome" class="block text-sm font-medium text-gray-700"
          >Nome no Cartão <span class="text-red-600">*</span></label
        >
        <InputText
          id="nome"
          v-model="form.name"
          required
          placeholder="Nome no Cartão"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-700"
          >E-mail <span class="text-red-600">*</span></label
        >
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
        <label for="numero_cartao" class="block text-sm font-medium text-gray-700"
          >Número do Cartão <span class="text-red-600">*</span></label
        >
        <InputText
          id="numero_cartao"
          v-mask="'#### #### #### ####'"
          v-model="form.numero_cartao"
          required
          placeholder="Número do Cartão"
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <div class="grid grid-cols-2 gap-4">

        <div class="form-group">
          <label for="validade" class="block text-sm font-medium text-gray-700"
            >Data de Expiração <span class="text-red-600">*</span></label
          >
          <InputText
            id="validade"
            v-mask="'##/##'"
            v-model="form.validade"
            required
            placeholder="MM/AA"
            class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
          />
        </div>

        <div class="form-group">
          <label for="cvv" class="block text-sm font-medium text-gray-700">CVV <span class="text-red-600">*</span>
          </label>
          <InputText
            id="cvv"
            v-mask="'###'"
            v-model="form.cvv"
            required
            placeholder="CVV"
            class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
          />
        </div>
      </div>

      <Button
        label="Processar Pagamento"
        type="submit"
        :loading="loading"
        icon="pi pi-credit-card"
        class="mt-5 my-10 w-full button-primary"
      />

      <div class="text-center text-primary font-bold underline">
        <router-link :to="{name: 'home'}">Realizar Pagamento com Pix</router-link>
      </div>

    </form>
  </div>
</template>

<script setup>
import { onUnmounted, ref } from 'vue'
import axios from 'axios'
import { InputText, Button, useToast } from 'primevue'
import { useRoute, useRouter } from 'vue-router';
import { doc, onSnapshot } from 'firebase/firestore';
import { db } from '@/firebase';
import { onMounted } from 'vue';


const route = useRoute()
const router = useRouter()
const loading = ref(false)
const form = ref({
  name: '',
  email: '',
  numero_cartao: '',
  validade: '',
  cvv: '',
})
const payment = ref(null)
const toast = useToast()

const processarPagamento = async () => {
  loading.value = true

  try {
    const { data } = await axios.post(`${import.meta.env.VITE_EXTERNAL_API}demo-criar-pagamento-cartao`, {
      ...form.value,
      numero_cartao: form.value.numero_cartao.replace(/\s/g, ''),
      amount: payment.value.donationAmount,
      id_ref: code
    })

    toast.add({
      severity: 'success',
      summary: data?.mensagem,
      detail: `Pagamento de R$ ${payment.value.donationAmount / 100} confirmado!`,
      life: 5000,
    })
    return router.push({ name: 'success' })
  } catch (error) {
    console.log(error);
    toast.add({
      severity: 'error',
      summary: 'Erro ao Processar Pagamento',
      detail: error?.response?.data?.mensagem || 'Ocorreu um erro ao tentar processar o pagamento.',
      life: 10000,
    })
  } finally {
    loading.value = false
  }
}



const code = route.params.code
const fetchPaymentRealTime = () => {
  const paymentDocRef = doc(db, 'payments', code)
  const unsubscribe = onSnapshot(paymentDocRef, (docSnap) => {
    if (docSnap.exists()) {
      payment.value = docSnap.data()

      if (payment.value.status === 'Pago') {
        router.push({ name: 'success' })
      }
    } else {
      console.log('Pagamento não encontrado!')
      payment.value = null
    }
  })

  onUnmounted(() => {
    unsubscribe()
  })
}

onMounted(async () => {
  fetchPaymentRealTime()
})
</script>
