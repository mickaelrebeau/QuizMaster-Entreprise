<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded shadow w-full max-w-sm">
      <h2 class="text-2xl font-bold mb-6 text-center text-black">Connexion RH</h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block mb-1 text-left text-black">Email</label>
          <input v-model="email" type="email"
            class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            required />
        </div>
        <div class="mb-6  text-black">
          <label class="block mb-1 text-left text-black">Mot de passe</label>
          <div class="relative">
            <input v-model="password" :type="showPassword ? 'text' : 'password'"
              class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              required />
            <button type="button" @click="showPassword = !showPassword" tabindex="-1"
              class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 focus:outline-none bg-transparent border-none p-0 m-0 appearance-none shadow-none"
              style="background:transparent;border:none;padding:0;margin:0;box-shadow:none;">
              <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
            </button>
          </div>
        </div>
        <p v-if="error" class="text-red-500 mt-2 text-left">{{ error }}</p>
        <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition w-full">Se
          connecter</button>
        <p class="text-center text-gray-500 mt-4">Vous n'avez pas de compte ? <router-link to="/register"
            class="text-blue-500 hover:text-blue-700">Créer un compte</router-link></p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Eye, EyeOff } from 'lucide-vue-next'
const email = ref('')
const password = ref('')
const error = ref('')
const showPassword = ref(false)
const router = useRouter()

async function login() {
  error.value = ''
  try {
    const res = await fetch('http://localhost:8000/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        username: email.value,
        password: password.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      localStorage.setItem('token', data.access_token)
      router.push('/dashboard')
    } else {
      error.value = data.detail || 'Erreur de connexion'
    }
  } catch (e) {
    error.value = 'Erreur serveur'
  }
}
</script>