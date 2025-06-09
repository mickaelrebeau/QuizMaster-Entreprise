<template>
  <div class="bg-white rounded-lg shadow p-6 flex flex-col">
    <h2 class="text-2xl font-bold mb-4">Résultats des quiz</h2>
    <form @submit.prevent="fetchResultats" class="mb-6 flex gap-2">
      <input v-model="quizId" placeholder="ID du quiz" class="px-2 py-1 border rounded" required />
      <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Voir les résultats</button>
    </form>
    <ul>
      <li v-for="res in resultats" :key="res.id" class="mb-2 p-2 border rounded">
        Score : <strong>{{ res.score }}</strong> — Date : {{ new Date(res.date).toLocaleString() }}
        <button @click="voirReponses(res)"
          class="ml-4 px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition">Voir réponses</button>
      </li>
    </ul>
    <div v-if="resultatsFetched && resultats.length === 0" class="text-center text-gray-500 mt-4">
      Aucun résultat trouvé pour ce quiz.
    </div>
    <div v-if="showDetail"
      class="fixed inset-0 flex items-center justify-center bg-black/50 z-50 overflow-y-auto"
      @click.self="fermerDetail" @keydown.esc="fermerDetail" tabindex="0">
      <div class="bg-white mt-8 p-6 rounded shadow w-full max-w-2xl max-h-[90vh] overflow-y-auto relative">
        <button @click="fermerDetail"
          class="absolute top-2 right-2 text-gray-500 hover:text-black p-2 rounded-full hover:bg-gray-100 transition">
          ✕
        </button>
        <h3 class="text-lg font-bold mb-4">Réponses détaillées du candidat</h3>
        <ul>
          <li v-for="(rep, idx) in reponsesDetaillees" :key="idx" class="mb-3 p-2 border rounded">
            <div class="font-semibold">Q : {{ rep.question }}</div>
            <div
              :class="{ 'text-green-700': rep.reponse_choisie === rep.bonne_reponse, 'text-red-700': rep.reponse_choisie !== rep.bonne_reponse }">
              Réponse choisie : <strong>{{ rep.reponse_choisie }}</strong>
            </div>
            <div v-if="rep.bonne_reponse && rep.reponse_choisie !== rep.bonne_reponse" class="text-green-700">
              Bonne réponse : <strong>{{ rep.bonne_reponse }}</strong>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const quizId = ref('')
const resultats = ref([])
const resultatsFetched = ref(false)
const showDetail = ref(false)
const reponsesDetaillees = ref([])

function handleEscape(e) {
  if (e.key === 'Escape' && showDetail.value) {
    fermerDetail()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleEscape)
})

async function fetchResultats() {
  const res = await fetch(`http://localhost:8000/quiz/${quizId.value}/resultats`)
  if (res.ok) {
    resultats.value = await res.json()
  } else {
    resultats.value = []
  }
  resultatsFetched.value = true
}

async function voirReponses(res) {
  const token = prompt('Entrer le token du candidat pour ce résultat :')
  if (!token) return
  const r = await fetch(`http://localhost:8000/candidat/quiz/${token}/reponses-detaillees`)
  if (r.ok) {
    reponsesDetaillees.value = await r.json()
    showDetail.value = true
  }
}

function fermerDetail() {
  showDetail.value = false
  reponsesDetaillees.value = []
}
</script>