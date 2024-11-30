<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold">Tela de Pagamento</h1>
        <p class="text-gray-600 mt-2">Sua doação faz a diferença!</p>
      </div>

      <div class="mb-6">
        <div class="flex justify-center space-x-4">
          <button
            @click="paymentMethod = 'card'"
            :class="{
              'bg-primary text-white': paymentMethod === 'card',
              'bg-gray-200 text-gray-700': paymentMethod !== 'card',
            }"
            class="px-4 py-2 rounded-lg font-medium transition duration-200"
          >
            <CreditCardIcon class="inline-block mr-2 h-5 w-5" />
            Cartão
          </button>
          <button
            @click="paymentMethod = 'pix'"
            :class="{
              'bg-primary text-white': paymentMethod === 'pix',
              'bg-gray-200 text-gray-700': paymentMethod !== 'pix',
            }"
            class="px-4 py-2 rounded-lg font-medium transition duration-200"
          >
            <QrCodeIcon class="inline-block mr-2 h-5 w-5" />
            PIX
          </button>
        </div>
      </div>

       <form v-if="paymentMethod === 'card'" @submit.prevent="processCardPayment">
        <div class="mb-2">
          <label for="cardholderName" class="block text-sm font-medium text-gray-700 mb-1">
            Nome no Cartão <span class="text-red-600">*</span>
          </label>
          <InputText
            type="text"
            id="cardholderName"
            v-model="form.name"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="João da Silva"
            required
          />
        </div>

        <div class="mb-2">
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

        <div class="mb-2">
          <label for="cardNumber" class="block text-sm font-medium text-gray-700 mb-1">
            Número do Cartão <span class="text-red-600">*</span>
          </label>
          <InputText
            type="text"
            id="cardNumber"
            v-mask="'#### #### #### ####'"
            v-model="form.card_number"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="1234 5678 9012 3456"
            required
          />
        </div>

        <div class="mb-4 flex space-x-4">
          <div class="w-1/2">
            <label for="expiryDate" class="block text-sm font-medium text-gray-700 mb-1">
              Data de Expiração <span class="text-red-600">*</span>
            </label>
            <InputText
              type="text"
              id="expiryDate"
              v-mask="'##/##'"
              v-model="form.expiration_date"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="MM/AA"
              required
            />
          </div>
          <div class="w-1/2">
            <label for="cvv" class="block text-sm font-medium text-gray-700 mb-1">CVV <span class="text-red-600">*</span></label>
            <InputText
              type="text"
              id="cvv"
              v-mask="'###'"
              v-model="form.cvv"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="123"
              required
            />
          </div>
        </div>

        <Button
          type="submit"
          label="Doar com Cartão"
          icon="pi pi-heart"
          :loading="loading"
          class="w-full button-primary transition duration-200"
        />
      </form>

      <div v-else-if="paymentMethod === 'pix'" class="text-center">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <i class="pi pi-spin pi-spinner text-primary text-4xl"></i>
        </div>

        <form v-if="!qrCode && !loading" @submit.prevent="generatePixCode" class="space-y-4">
          <div class="form-group">
            <label for="nome" class="block text-sm font-medium text-gray-700 text-start">Nome <span class="text-red-600">*</span></label>
            <InputText id="nome" v-model="form.name" required placeholder="Nome do Cliente" class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"/>
          </div>

          <div class="form-group">
            <label for="email" class="block text-sm font-medium text-gray-700 text-start">E-mail <span class="text-red-600">*</span></label>
            <InputText id="email" v-model="form.email" type="email" required placeholder="E-mail" class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary" />
          </div>

          <div class="form-group">
            <label for="cpf" class="block text-sm font-medium text-gray-700 text-start">CPF <span class="text-red-600">*</span></label>
            <InputText id="cpf" v-mask="'###.###.###-##'" placeholder="CPF (111.111.111-11)" v-model="form.cpf" required class="mt-1 block w-full hover:border-primary focus:border-primary active:border-primary"/>
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

      <div class="mt-6 text-center text-sm text-gray-600">
        <p>Sua doação ajuda a manter nossos projetos. Obrigado pelo seu apoio!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { CreditCardIcon, QrCodeIcon } from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import { InputText, Button, useToast } from 'primevue'
import axios from 'axios'
import { addDoc, collection } from 'firebase/firestore'
import QrcodeVue from 'qrcode.vue'
import { db } from '@/firebase'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const form = ref({
  name: '',
  email: '',
  card_number: '',
  expiration_date: '',
  amount: route.query.amount,
  cvv: '',
  cpf: ''
})
const qrCode = ref(null)
const payment = ref(null)
const paymentMethod = ref('card')
const toast = useToast()

const processCardPayment = async () => {
  loading.value = true

  try {
    const ipResponse = await fetch('https://api.ipify.org?format=json')
    const ipData = await ipResponse.json()
    const userIP = ipData.ip

    const paysCollection = collection(db, 'payments')
    const docRef = await addDoc(paysCollection, {
      ...form.value,
      browserInfo: navigator.userAgent,
      userIP: userIP,
    })

    const { data } = await axios.post(
      `${import.meta.env.VITE_EXTERNAL_API}${import.meta.env.VITE_APP_API}-payment-card`,
      {
        ...form.value,
        cpf: form.value.cpf.replace(/[^\d]/g, ''),
        id_ref: docRef.id,
      }
    )

    payment.value = data
    toast.add({
      severity: 'success',
      summary: 'Sucesso',
      detail: 'Pagamento efetuado com sucesso',
    })
    return router.push({ name: 'success' })
  } catch (error) {
    console.error(error)
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: error?.response?.data?.error
    })
  } finally {
    loading.value = false
  }
}

const generatePixCode = async () => {
  loading.value = true
  try {
    const ipResponse = await fetch('https://api.ipify.org?format=json')
    const ipData = await ipResponse.json()
    const userIP = ipData.ip

    const paysCollection = collection(db, 'payments')
    const docRef = await addDoc(paysCollection, {
      ...form.value,
      browserInfo: navigator.userAgent,
      userIP: userIP,
    })

    const { data } = await axios.post(`${import.meta.env.VITE_EXTERNAL_API}${import.meta.env.VITE_APP_API}-payment-pix`, {
      ...form.value,
      card_number: form.value.card_number.replace(/\s+/g, ''),
      expiration_date: form.value.expiration_date.replace(/\D/g, ''),
      cpf: form.value.cpf.replace(/[^\d]/g, ''),
      id_ref: docRef.id,
    })
    qrCode.value = data.qrcode
  } catch (error) {
    console.error(error)
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: error?.response?.data?.error
    })
  } finally {
    loading.value = false
  }
}

const copiarQRCode = async () => {
  try {
    await navigator.clipboard.writeText(qrCode.value)
    toast.add({
      severity: 'success',
      summary: 'Copiado',
      detail: 'Código Pix copiado com sucesso!',
    })
  } catch (error) {
    console.error('Erro ao copiar o código Pix:', error)
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Falha ao copiar o código Pix',
    })
  }
}
</script>
