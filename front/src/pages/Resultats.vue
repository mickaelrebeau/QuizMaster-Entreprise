<template>
  <div class="bg-white rounded-lg shadow p-6 mt-12 flex flex-col">
    <h2 class="text-2xl font-bold mb-4">Résultats des quiz</h2>
    <form @submit.prevent="fetchResultats" class="mb-6 flex gap-2">
      <input v-model="quizId" placeholder="ID du quiz" class="px-2 py-1 border rounded" required />
      <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Voir les résultats</button>
    </form>
    <ul>
      <li v-for="res in resultats" :key="res.id" class="mb-2 p-2 border rounded flex justify-between">
        <p>Score : <strong>{{ res.score }}</strong> — Date : {{ new Date(res.date).toLocaleString() }}</p>
        <button @click="ouvrirModalToken(res)"
          class="ml-4 px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition">Voir les
          réponses</button>
      </li>
    </ul>
    <div v-if="resultatsFetched && resultats.length === 0" class="text-center text-gray-500 mt-4">
      Aucun résultat trouvé pour ce quiz.
    </div>

    <!-- Modal pour les réponses détaillées -->
    <ReponsesDetailleesModal v-model="showDetail" :reponses="reponsesDetaillees"/>

    <!-- Modal pour le token -->
    <Modal v-model="showTokenModal" title="Entrer le token">
      <form @submit.prevent="soumettreToken" class="flex flex-col gap-4">
        <input v-model="tokenInput" placeholder="Token du candidat" class="px-2 py-1 border rounded" required />
        <div class="flex justify-end gap-2">
          <button type="button" @click="fermerTokenModal"
            class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 transition">
            Annuler
          </button>
          <button type="submit" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            Valider
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Modal from '../components/Modal.vue'
import ReponsesDetailleesModal from '../components/ReponsesDetailleesModal.vue'

const quizId = ref('')
const resultats = ref([])
const resultatsFetched = ref(false)
const showDetail = ref(false)
const reponsesDetaillees = ref([])
const showTokenModal = ref(false)
const tokenInput = ref('')
const resultatSelectionne = ref(null)

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

function ouvrirModalToken(res) {
  resultatSelectionne.value = res
  showTokenModal.value = true
  tokenInput.value = ''
}

function fermerTokenModal() {
  showTokenModal.value = false
  tokenInput.value = ''
  resultatSelectionne.value = null
}

async function soumettreToken() {
  if (!tokenInput.value) return
  const r = await fetch(`http://localhost:8000/candidat/quiz/${tokenInput.value}/reponses-detaillees`)
  if (r.ok) {
    reponsesDetaillees.value = await r.json()
    showDetail.value = true
    fermerTokenModal()
  } else {
    alert('Token invalide')
  }
}

function fermerDetail() {
  showDetail.value = false
  reponsesDetaillees.value = []
}
</script>