<template>
  <div class="p-5">
    <h1 class="text-3xl font-bold mb-2 text-start">Faça Sua Doação via Pix</h1>
    <h2 class="text-xl font-medium mb-6 text-start text-gray-600">
      Sua doação ajuda a transformar vidas. Contribua para um futuro melhor.
    </h2>

    <form v-if="!qrCode && payment" @submit.prevent="gerarQRCode" class="space-y-4">
      <div class="form-group">
        <label for="nome" class="block text-sm font-medium text-gray-700">Nome do Cliente</label>
        <InputText
          id="nome"
          v-model="form.name"
          required
          placeholder="Nome do Cliente"
          class="mt-1 block w-full input-base"
        />
      </div>

      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-700">E-mail</label>
        <InputText
          id="email"
          v-model="email"
          type="email"
          required
          placeholder="E-mail"
          class="mt-1 block w-full input-base"
        />
      </div>

      <div class="form-group">
        <label for="valor" class="block text-sm font-medium text-gray-700">CPF</label>
        <InputText
          id="valor"
          v-mask="'###.###.###-##'"
          v-model="valor"
          required
          class="mt-1 block w-full input-base"
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
import { ref, onMounted } from 'vue'
import { doc, getDoc, updateDoc } from 'firebase/firestore'
import QrcodeVue from 'qrcode.vue'
import { InputText, Button, useToast } from 'primevue'
import { db } from '../firebase'
import { useRoute } from 'vue-router'
import axios from 'axios'

const payment = ref(null)

const toast = useToast()
const loading = ref(false)
const form = ref({
  email: '',
  name: '',
  amount: '',
})
const email = ref('')
const valor = ref('')
const qrCode = ref(null)

const fetchPayment = async (code) => {
  try {
    const paymentDocRef = doc(db, 'pays', code)
    const docSnap = await getDoc(paymentDocRef)

    if (docSnap.exists()) {
      payment.value = docSnap.data()
    } else {
      console.log('Pagamento não encontrado!')
      payment.value = null
    }
  } catch (error) {
    console.error('Erro ao buscar pagamento:', error)
  }
}

const gerarQRCode = async () => {
  loading.value = true
  const pixData = {
    name: form.value.name,
    amount: payment.value.donationAmount,
    email: form.value.email,
  }

  axios
    .post(`${import.meta.env.VITE_EXTERNAL_API}payment`, {
      ...pixData,
      id_ref: 'HSHda4VRjcIcJ1tCLRtb',
    })
    .then(({ data }) => {
      updateDoc(code, form.value)

      qrCode.value = data['pix']
      toast.add({
        severity: 'info',
        summary: 'Pix Gerado com Sucesso',
        detail: 'Realize seu Pagamento',
        life: 5000,
      })
    })
    .catch((response) => {
      toast.add({
        severity: 'error',
        detail: 'Error ao Gerar Pix',
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
          detail: 'Seu codigo foi copiado para area de trasnferencia',
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

const code = useRoute().params.code
onMounted(async () => {
  await fetchPayment(code)
})
</script>
