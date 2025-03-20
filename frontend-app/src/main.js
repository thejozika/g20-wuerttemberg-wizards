import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'

import HomeView from './views/HomeView.vue'
import DashboardView from './views/DashboardView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/dashboard', component: DashboardView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).mount('#app')
