<template>
  <div class="p-5">
    <h1 class="text-3xl font-bold mb-2 text-start">Faça Sua Doação via Pix</h1>
    <h2 class="text-xl font-medium mb-6 text-start text-gray-600">
      Sua doação ajuda a transformar vidas. Contribua para um futuro melhor.
    </h2>

    <div v-if="loading" class="flex justify-center items-center h-64">
      <i class="pi pi-spin pi-spinner text-4xl"></i>
    </div>

    <form v-if="!qrCode && payment && !loading" @submit.prevent="gerarQRCode" class="space-y-4">
      <div class="form-group">
        <label for="nome" class="block text-sm font-medium text-gray-700">Nome <span class="text-red-600">*</span></label>
        <InputText
          id="nome"
          v-model="form.name"
          required
          placeholder="Nome do Cliente"
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
        <label for="document" class="block text-sm font-medium text-gray-700">CPF <span class="text-red-600">*</span></label>
        <InputText
          id="document"
          v-mask="'###.###.###-##'"
          placeholder="CPF (111.111.111-11)"
          v-model="form.document"
          required
          class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"
        />
      </div>

      <Button
        label="Gerar QR Code"
        type="submit"
        :loading="loading"
        icon="pi pi-qrcode"
        class="w-full button-primary"
      />
    </form>

    <div v-if="qrCode" class="mt-8 text-center">
      <h3 class="text-xl font-semibold mb-4">QR Code Pix</h3>
      <qrcode-vue :value="qrCode" :size="200" level="H" class="mx-auto" />

      <p class="my-8" @click="copiarQRCode">{{ qrCode }}</p>

      <div class="mt-4">
        <Button
          @click="copiarQRCode"
          icon="pi pi-clipboard"
          label="Copiar Código"
          class="w-full text-white button-primary"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { doc, onSnapshot, updateDoc } from 'firebase/firestore'
import QrcodeVue from 'qrcode.vue'
import { InputText, Button, useToast } from 'primevue'
import { db } from '../firebase'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const payment = ref(null)

const toast = useToast()
const loading = ref(false)
const form = ref({
  email: '',
  name: '',
  amount: '',
  document: '',
})
const qrCode = ref(null)

const route = useRoute()
const router = useRouter()

const gerarQRCode = async () => {
  loading.value = true

  axios
    .post(`${import.meta.env.VITE_EXTERNAL_API}payment`, {
      ...form.value,
      amount: payment.value.donationAmount,
      cpf: form.value.document.replace(/[^\d]/g, ''),
      id_ref: code
    })
    .then(async ({ data }) => {
      const paymentDocRef = doc(db, 'payments', code)
      await updateDoc(paymentDocRef, form.value)

      qrCode.value = data['pix']
      toast.add({
        severity: 'info',
        summary: 'Pix Gerado com Sucesso',
        detail: 'Realize seu Pagamento',
        life: 5000,
      })
    })
    .catch((response) => {
      console.log(response);
      toast.add({
        severity: 'error',
        summary: 'Erro ao Gerar Pix',
        detail: response?.response?.data?.error,
        life: 5000,
      })
    })
    .finally(() => (loading.value = false))
}

const copiarQRCode = () => {
  if (qrCode.value) {
    navigator.clipboard
      .writeText(qrCode.value)
      .then(() => {
        toast.add({
          severity: 'success',
          summary: 'Código Copiado!',
          detail: 'Seu código foi copiado para área de transferência',
          life: 3000,
        })
      })
      .catch(() => {
        toast.add({
          severity: 'error',
          summary: 'Falha ao Copiar',
          life: 3000,
        })
      })
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
