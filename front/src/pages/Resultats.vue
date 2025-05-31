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
      </li>
    </ul>
    <div v-if="resultatsFetched && resultats.length === 0" class="text-center text-gray-500 mt-4">
      Aucun résultat trouvé pour ce quiz.
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const quizId = ref('')
const resultats = ref([])
const resultatsFetched = ref(false)

async function fetchResultats() {
  const res = await fetch(`http://localhost:8000/quiz/${quizId.value}/resultats`)
  if (res.ok) {
    resultats.value = await res.json()
  } else {
    resultats.value = []
  }
  resultatsFetched.value = true
}
</script>