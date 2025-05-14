<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold mb-6">Tableau de bord RH</h1>
    <nav class="mb-8 flex gap-4">
      <router-link to="/fiches" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Fiches de
        poste</router-link>
      <router-link to="/quiz" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Générer un
        quiz</router-link>
      <router-link to="/quiz-list" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Liste
        des quiz</router-link>
      <router-link to="/resultats"
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Résultats</router-link>
      <button @click="logout"
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Déconnexion</button>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
const router = useRouter()

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token || isTokenExpired(token)) {
    logout()
  }
})
</script>