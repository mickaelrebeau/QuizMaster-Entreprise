<template>
    <div class="bg-white rounded-lg shadow p-6 mt-12 flex flex-col">
        <h2 class="text-2xl font-bold mb-4">Liste des quiz générés</h2>
        <ul>
            <li v-for="quiz in quizzes" :key="quiz.id" class="mb-4 p-4 border rounded">
                <div class="flex justify-between items-center">
                    <div class="flex flex-col mr-8 text-left">
                        <strong>{{ quiz.titre }}</strong>
                        <span class="text-gray-600">Quiz ID : {{ quiz.id }}</span>
                        <span class="text-gray-600">Fiche de poste ID : {{ quiz.fiche_poste_id }}</span>
                    </div>
                    <div class="flex gap-2">
                        <button @click="voirQuiz(quiz.id)"
                            class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Voir</button>
                        <button @click="ouvrirModalLien(quiz.id)"
                            class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition">Générer lien
                            candidat</button>
                        <button @click="supprimerQuiz(quiz.id)"
                            class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition">Supprimer</button>
                    </div>
                </div>
            </li>
        </ul>

        <!-- Modal pour générer un lien -->
        <Modal v-model="showModal" title="Générer un lien pour un candidat">
            <form @submit.prevent="genererLienCandidat">
                <input v-model="emailCandidat" type="email" placeholder="Email du candidat"
                    class="px-2 py-1 border rounded w-full mb-2" required />
                <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition w-full">Générer
                    le lien</button>
            </form>
            <div v-if="lienCandidat" class="mt-2">
                <p>Lien généré :</p>
                <input :value="lienCandidat" readonly class="w-full px-2 py-1 border rounded bg-gray-100" />
            </div>
            <template #footer>
                <button @click="fermerModal"
                    class="px-3 py-1 bg-gray-400 text-white rounded hover:bg-gray-500 transition w-full">Fermer</button>
            </template>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Modal from '../components/Modal.vue'

const quizzes = ref([])
const showModal = ref(false)
const quizIdPourLien = ref(null)
const emailCandidat = ref('')
const lienCandidat = ref('')
const router = useRouter()

function handle401(res) {
    if (res.status === 401) {
        localStorage.removeItem('token')
        router.push('/login')
        return true
    }
    return false
}

async function fetchQuizzes() {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/quizzes', {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if (handle401(res)) return
    if (res.ok) {
        quizzes.value = await res.json()
    }
}
onMounted(fetchQuizzes)

function voirQuiz(id) {
    router.push(`/quiz/${id}`)
}

function ouvrirModalLien(id) {
    quizIdPourLien.value = id
    emailCandidat.value = ''
    lienCandidat.value = ''
    showModal.value = true
}

function fermerModal() {
    showModal.value = false
}

async function genererLienCandidat() {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/candidat/lien', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ quiz_id: quizIdPourLien.value, email: emailCandidat.value })
    })
    if (handle401(res)) return
    if (res.ok) {
        const data = await res.json()
        lienCandidat.value = window.location.origin + data.lien
    }
}

async function supprimerQuiz(id) {
    if (!confirm('Voulez-vous vraiment supprimer ce quiz ?')) return;
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:8000/quiz/${id}`, {
        method: 'DELETE',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if (handle401(res)) return
    if (res.ok) {
        quizzes.value = quizzes.value.filter(q => q.id !== id)
    } else {
        alert('Erreur lors de la suppression du quiz.')
    }
}
</script>