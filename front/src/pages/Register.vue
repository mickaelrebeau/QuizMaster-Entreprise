<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded shadow w-full max-w-sm">
      <h2 class="text-2xl font-bold mb-6 text-center text-black">Créer un compte RH</h2>
      <form @submit.prevent="register">
        <div class="mb-4">
          <label class="block mb-1 text-left text-black">Email</label>
          <input v-model="email" type="email"
            class="w-full ps-3 pe-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            required />
        </div>
        <div class="mb-4">
          <label class="block mb-1 text-left text-black">Mot de passe</label>
          <div class="relative">
            <input v-model="password" :type="showPassword ? 'text' : 'password'"
              class="w-full ps-3 pe-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              required />
            <button type="button" @click="showPassword = !showPassword" tabindex="-1"
              class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 focus:outline-none bg-transparent border-none p-0 m-0 appearance-none shadow-none"
              style="background:transparent;border:none;padding:0;margin:0;box-shadow:none;">
              <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
            </button>
          </div>
        </div>
        <div class="mb-6">
          <label class="block mb-1 text-left text-black">Confirmer le mot de passe</label>
          <div class="relative">
            <input v-model="confirm" :type="showConfirm ? 'text' : 'password'"
              class="w-full ps-3 pe-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              required />
            <button type="button" @click="showConfirm = !showConfirm" tabindex="-1"
              class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 focus:outline-none bg-transparent border-none p-0 m-0 appearance-none shadow-none"
              style="background:transparent;border:none;padding:0;margin:0;box-shadow:none;">
              <component :is="showConfirm ? EyeOff : Eye" class="w-5 h-5" />
            </button>
          </div>
        </div>
        <p v-if="error" class="text-red-500 mt-2 text-left">{{ error }}</p>
        <p v-if="success" class="text-green-600 mt-2 text-left">{{ success }}</p>
        <button type="submit"
          class="ps-4 pe-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition w-full">Créer le
          compte</button>
        <p class="text-center text-gray-500 mt-4">Vous avez déjà un compte ? <router-link to="/login"
            class="text-blue-500 hover:text-blue-700">Connectez-vous</router-link></p>
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
const confirm = ref('')
const error = ref('')
const success = ref('')
const showPassword = ref(false)
const showConfirm = ref(false)
const router = useRouter()

async function register() {
  error.value = ''
  success.value = ''
  if (password.value !== confirm.value) {
    error.value = 'Les mots de passe ne correspondent pas.'
    return
  }
  try {
    const res = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value, is_rh: true })
    })
    if (res.ok) {
      success.value = 'Compte créé ! Vous pouvez vous connecter.'
      setTimeout(() => router.push('/login'), 1500)
    } else {
      const data = await res.json()
      error.value = data.detail || 'Erreur lors de la création du compte.'
    }
  } catch (e) {
    error.value = 'Erreur serveur.'
  }
}
</script>
