<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Fiches de poste</h2>
    <form @submit.prevent="createFiche" class="mb-6 flex gap-2">
      <input v-model="titre" placeholder="Titre" class="px-2 py-1 border rounded" required />
      <input v-model="entreprise" placeholder="Entreprise" class="px-2 py-1 border rounded" required />
      <input v-model="description" placeholder="Description" class="px-2 py-1 border rounded" required />
      <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Ajouter</button>
    </form>
    <ul>
      <li v-for="fiche in fiches" :key="fiche.id" class="mb-2 p-2 border rounded">
        <strong>{{ fiche.titre }}</strong> — {{ fiche.entreprise }}<br />
        <span class="text-sm text-gray-500">{{ fiche.description }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const fiches = ref([])
const titre = ref('')
const entreprise = ref('')
const description = ref('')
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
  }
}
</script>