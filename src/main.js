import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import moment from 'moment';
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { VueFireAuth, VueFireFirestoreOptionsAPI, VueFireDatabaseOptionsAPI, VueFire } from 'vuefire'

import App from './App.vue'
import router from './router'

import VueTheMask from 'vue-the-mask'
import money from 'v-money'
import 'flowbite';
import 'primeicons/primeicons.css'
import { firebaseApp } from './firebase'


import VueBarcode from '@chenfengyuan/vue-barcode';


import { ConfirmationService } from 'primevue';


import ToastService from 'primevue/toastservice';

import 'moment/locale/pt-br';
moment.locale('pt-br');

import { currencyBR } from './utils/FormatMonetaryValue';

const app = createApp(App)
app.config.globalProperties.$moment = moment;
app.config.globalProperties.$amount = currencyBR;


app.use(ToastService)
app.use(ConfirmationService)


app.use(VueFire, {
  firebaseApp,
  modules: [
    VueFireAuth(),
    VueFireFirestoreOptionsAPI(),
    VueFireDatabaseOptionsAPI(),
  ]
})

app.use(createPinia())
  .use(PrimeVue, {
    theme: {
      preset: Aura,
      options: {
        cssLayer: {
          name: 'primevue',
          order: 'tailwind-base, primevue, tailwind-utilities',
        },
        darkModeSelector: false,
      },
    }
  })
  .use(VueTheMask)
  .use(money)
  .use(router)
  .component(VueBarcode.name, VueBarcode)
  .mount('#app')
