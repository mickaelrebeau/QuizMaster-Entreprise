<template>
    <div v-if="quiz" class="bg-white rounded-lg shadow p-6 mt-12 flex flex-col">
        <h2 class="text-2xl font-bold mb-4">Détail du quiz : {{ quiz.titre }}</h2>
        <div class="mb-2 text-gray-600">ID : {{ quiz.id }} | Fiche de poste ID : {{ quiz.fiche_poste_id }}</div>
        <ul>
            <li v-for="q in quiz.questions" :key="q.id" class="mb-4 p-2 border rounded text-left">
                <div class="font-semibold mb-1">Question : {{ q.texte }}</div>
                <ul class="ml-4 mt-4">
                    <li v-for="r in q.reponses || []" :key="r.id" class="text-gray-700">
                        - {{ r.texte }} <span v-if="r.is_correct" class="text-green-600 font-bold">(Bonne
                            réponse)</span>
                    </li>
                </ul>
                <div v-if="reponsesCandidats[q.id] && reponsesCandidats[q.id].length" class="mt-2">
                    <div class="font-semibold text-sm text-blue-700">Réponses des candidats :</div>
                    <ul class="ml-4">
                        <li v-for="(rep, idx) in reponsesCandidats[q.id]" :key="idx" class="text-sm">
                            - {{ rep }}
                        </li>
                    </ul>
                </div>
            </li>
        </ul>
        <button @click="retour"
            class="mt-4 px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500 transition">Retour</button>
    </div>
    <div v-else class="bg-white rounded-lg shadow p-6 flex flex-col">
        <p>Chargement...</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()
const quiz = ref(null)
const reponsesCandidats = ref({})

function handle401(res) {
    if (res.status === 401) {
        localStorage.removeItem('token')
        router.push('/login')
        return true
    }
    return false
}

onMounted(async () => {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:8000/quiz/${route.params.id}`, {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    console.log(res)
    if (handle401(res)) return
    if (res.ok) {
        quiz.value = await res.json()
        const res2 = await fetch(`http://localhost:8000/quiz/${route.params.id}/resultats`)
        if (res2.ok) {
            const resultats = await res2.json()
            const map = {}
            for (const resultat of resultats) {
                if (resultat.reponses_candidats) {
                    for (const rep of resultat.reponses_candidats) {
                        if (!map[rep.question_id]) map[rep.question_id] = []
                        map[rep.question_id].push(rep.texte)
                    }
                }
            }
            reponsesCandidats.value = map
        }
    }
})

function retour() {
    router.push('/quiz-list')
}
</script>