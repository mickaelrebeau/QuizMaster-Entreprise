<template>
    <div class="bg-white rounded-lg shadow p-6 mt-12">
        <h2 class="text-2xl font-bold mb-4">Liste des liens candidats</h2>
        <div class="overflow-x-auto">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="px-4 py-2 text-left">Email</th>
                        <th class="px-4 py-2 text-left">Quiz ID</th>
                        <th class="px-4 py-2 text-left">Token</th>
                        <th class="px-4 py-2 text-left">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="lien in liens" :key="lien.id" class="border-b">
                        <td class="px-4 py-2">{{ lien.email }}</td>
                        <td class="px-4 py-2">{{ lien.quiz_id }}</td>
                        <td class="px-4 py-2">
                            <code class="bg-gray-100 px-2 py-1 rounded">{{ lien.token }}</code>
                        </td>
                        <td class="px-4 py-2">
                            <button @click="copierToken(lien.token)"
                                class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
                                Copier
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="liens.length === 0" class="text-center text-gray-500 mt-4">
            Aucun lien candidat trouvé.
        </div>

        <!-- Modal de confirmation -->
        <Modal v-model="showModal" title="Confirmation">
            <p class="text-gray-700">{{ modalMessage }}</p>
            <template #footer>
                <button @click="showModal = false"
                    class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition w-full">
                    OK
                </button>
            </template>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Modal from '../components/Modal.vue'

const liens = ref([])
const showModal = ref(false)
const modalMessage = ref('')

async function fetchLiens() {
    try {
        const response = await fetch('http://localhost:8000/liens-candidats')
        if (response.ok) {
            liens.value = await response.json()
        }
    } catch (error) {
        console.error('Erreur lors de la récupération des liens:', error)
    }
}

function copierToken(token) {
    navigator.clipboard.writeText(token)
        .then(() => {
            modalMessage.value = 'Token copié dans le presse-papiers !'
            showModal.value = true
        })
        .catch(err => {
            console.error('Erreur lors de la copie:', err)
            modalMessage.value = 'Erreur lors de la copie du token'
            showModal.value = true
        })
}

onMounted(() => {
    fetchLiens()
})
</script>