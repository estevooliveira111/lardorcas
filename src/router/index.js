import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: '/payment/p/:code', name: 'payment_pix', component: () => import('../views/PaymentPixView.vue') },
    { path: '/payment/c/:code', name: 'payment_card', component: () => import('../views/PaymentCardView.vue') },
    { path: '/sucess', name: 'success', component: () => import('../views/SuccessView.vue') },
    { path: '/about', name: 'about', component: () => import('../views/AboutView.vue') },
  ]
})

export default router
