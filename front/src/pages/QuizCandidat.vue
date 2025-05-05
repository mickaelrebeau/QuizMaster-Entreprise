<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Quiz Candidat</h2>
    <div v-if="quiz">
      <form @submit.prevent="submit">
        <div v-for="q in quiz.questions" :key="q.id" class="mb-4">
          <div class="font-semibold mb-2">{{ q.texte }}</div>
          <input v-model="reponses[q.id]" placeholder="Votre réponse" class="px-2 py-1 border rounded" />
        </div>
        <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Envoyer mes
          réponses</button>
      </form>
      <div v-if="msg" class="mt-4 text-green-600">{{ msg }}</div>
    </div>
    <div v-else>
      <p>Chargement du quiz...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const quiz = ref(null)
const reponses = ref({})
const msg = ref('')

onMounted(async () => {
  const token = route.params.token
  const res = await fetch(`http://localhost:8000/candidat/quiz/${token}`)
  if (res.ok) {
    quiz.value = await res.json()
  }
})

async function submit() {
  // Ici, on envoie les réponses sous forme simplifiée (à adapter pour la gestion fine)
  msg.value = ''
  const token = route.params.token
  // Pour l'exemple, on envoie un score aléatoire
  const res = await fetch(`http://localhost:8000/candidat/quiz/${token}/repondre`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ score: Math.floor(Math.random()*10)+1 })
  })
  if (res.ok) {
    msg.value = 'Réponses envoyées !'
  }
}
</script>