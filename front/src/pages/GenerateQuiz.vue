<template>
  <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
    <h2 class="text-2xl font-bold mb-4">Générer un quiz</h2>
    <form @submit.prevent="generateQuiz" class="mb-6 flex gap-2">
      <select v-model="ficheId" class="px-2 py-1 border rounded" required>
        <option value="" disabled>Sélectionner une fiche de poste</option>
        <option v-for="fiche in fiches" :key="fiche.id" :value="fiche.id">
          {{ fiche.titre }} ({{ fiche.entreprise }})
        </option>
      </select>
      <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Générer</button>
    </form>
    <div v-if="quizId" class="mt-4">
      <p>Quiz généré avec l'ID : <strong>{{ quizId }}</strong></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const fiches = ref([])
const ficheId = ref('')
const quizId = ref('')
const router = useRouter()

function handle401(res) {
  if (res.status === 401) {
    localStorage.removeItem('token')
    router.push('/login')
    return true
  }
  return false
}

async function fetchFiches() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/fiches-poste', {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  })
  if (handle401(res)) return
  if (res.ok) {
    fiches.value = await res.json()
  }
}
onMounted(fetchFiches)

async function generateQuiz() {
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/quiz/generer?fiche_id=${ficheId.value}`, {
    method: 'POST',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  })
  if (handle401(res)) return
  if (res.ok) {
    const data = await res.json()
    quizId.value = data.quiz_id
  }
}
</script>
