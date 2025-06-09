<template>
  <div class="bg-white rounded-lg shadow p-6 mt-12 flex flex-col items-center">
    <h2 class="text-2xl font-bold mb-4">Générer un quiz</h2>
    <form @submit.prevent="generateQuiz" class="mb-6 flex gap-2">
      <select v-model="ficheId" class="px-2 py-1 border rounded" required>
        <option value="" disabled>Sélectionner une fiche de poste</option>
        <option v-for="fiche in fiches" :key="fiche.id" :value="fiche.id">
          {{ fiche.titre }} ({{ fiche.entreprise }})
        </option>
      </select>
      <button :disabled="loading"
        class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition flex items-center">
        <span v-if="!loading">Générer</span>
        <span v-else class="flex items-center"><svg class="animate-spin h-5 w-5 mr-2 text-white"
            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
          </svg>Génération...</span>
      </button>
    </form>
    <div v-if="loading" class="w-full max-w-md mb-2">
      <div class="h-3 bg-gray-200 rounded-full overflow-hidden">
        <div class="h-full bg-blue-500 transition-all duration-300" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="text-blue-600 font-semibold mt-1 text-center">Génération du quiz en cours, cela peut prendre quelques
        secondes...</div>
    </div>
    <div v-if="quizId && !loading" class="mt-4">
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
const loading = ref(false)
const progress = ref(0)
let progressInterval = null
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

function startProgress() {
  progress.value = 0
  if (progressInterval) clearInterval(progressInterval)
  progressInterval = setInterval(() => {
    // Simule une progression lente, puis ralentit à la fin
    if (progress.value < 90) {
      progress.value += Math.random() * 5 + 2 // avance rapide au début
    } else if (progress.value < 98) {
      progress.value += Math.random() * 1 // ralentit à la fin
    }
    if (progress.value > 98) progress.value = 98
  }, 200)
}
function stopProgress() {
  if (progressInterval) clearInterval(progressInterval)
  progress.value = 100
  setTimeout(() => { progress.value = 0 }, 1000)
}

async function generateQuiz() {
  loading.value = true
  quizId.value = ''
  startProgress()
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/quiz/generer?fiche_id=${ficheId.value}`, {
    method: 'POST',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  })
  if (handle401(res)) { loading.value = false; stopProgress(); return }
  if (res.ok) {
    const data = await res.json()
    quizId.value = data.quiz_id
  }
  loading.value = false
  stopProgress()
}
</script>
