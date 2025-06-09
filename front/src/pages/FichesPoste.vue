<template>
  <div class="p-8">
    <div class="flex justify-between items-center gap-8 mb-4">
      <h2 class="text-3xl font-bold">Fiches de poste</h2>

      <button @click="showModal = true" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
        Ajouter une fiche
      </button>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Nouvelle fiche de poste</h3>
          <button @click="showModal = false" class="text-gray-500 hover:text-gray-700">
            <span class="text-2xl">&times;</span>
          </button>
        </div>
        <form @submit.prevent="createFiche" class="flex flex-col gap-2">
          <input v-model="titre" placeholder="Titre" class="px-2 py-1 border rounded" required />
          <input v-model="entreprise" placeholder="Entreprise" class="px-2 py-1 border rounded" required />
          <textarea v-model="description" placeholder="Description" class="px-2 py-1 border rounded" required />
          <div class="flex justify-end gap-2 mt-4">
            <button type="button" @click="showModal = false"
              class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 transition">
              Annuler
            </button>
            <button type="submit" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
              Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="paginatedFiches.length === 0" class="mt-8 p-8 bg-white rounded-lg shadow text-center text-gray-500">
      Aucunes
      fiches de poste trouvée.</div>
    <div v-else class="mt-8 bg-white rounded-lg shadow p-6 flex flex-col">
      <h2 class="text-2xl font-bold mb-4">Liste des fiches de poste</h2>
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4 gap-2">
        <input v-model="search" placeholder="Rechercher par titre ou ID..."
          class="px-2 py-1 border rounded w-full md:w-64" />
        <div class="flex items-center gap-2 mt-2 md:mt-0">
          <button @click="prevPage" :disabled="page === 1"
            class="px-2 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:text-white disabled:opacity-50">Précédent</button>
          <span>Page {{ page }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="page === totalPages"
            class="px-2 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:text-white disabled:opacity-50">Suivant</button>
        </div>
      </div>
      <ul>
        <li v-for="fiche in paginatedFiches" :key="fiche.id" class="mb-2 p-2 border rounded text-left">
          <p class="text-lg text-center mb-4"><strong>{{ fiche.titre }}</strong> — {{ fiche.entreprise }} — {{ fiche.id
            }}<br /></p>
          <span class="text-sm text-gray-500 whitespace-pre-line">{{ fiche.description }}</span>
        </li>
      </ul>
      <div class="mt-8 flex flex-col md:flex-row md:items-center md:justify-end mb-4 gap-2">
        <div class="flex items-center gap-2 mt-2 md:mt-0">
          <button @click="prevPage" :disabled="page === 1"
            class="px-2 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:text-white disabled:opacity-50">Précédent</button>
          <span>Page {{ page }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="page === totalPages"
            class="px-2 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:text-white disabled:opacity-50">Suivant</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
const fiches = ref([])
const titre = ref('')
const entreprise = ref('')
const description = ref('')
const showModal = ref(false)
const router = useRouter()

const search = ref('')
const page = ref(1)
const perPage = 5

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

async function createFiche() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/fiche-poste', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify({ titre: titre.value, entreprise: entreprise.value, description: description.value })
  })
  if (handle401(res)) return
  if (res.ok) {
    fetchFiches()
    titre.value = ''
    entreprise.value = ''
    description.value = ''
    showModal.value = false
  }
}

const filteredFiches = computed(() => {
  if (!search.value.trim()) return fiches.value
  const s = search.value.trim().toLowerCase()
  return fiches.value.filter(f =>
    f.titre.toLowerCase().includes(s) || String(f.id).includes(s)
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredFiches.value.length / perPage)))
const paginatedFiches = computed(() => {
  const start = (page.value - 1) * perPage
  return filteredFiches.value.slice(start, start + perPage)
})

function prevPage() {
  if (page.value > 1) page.value--
}
function nextPage() {
  if (page.value < totalPages.value) page.value++
}

watch(search, () => { page.value = 1 })
</script>