<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Quiz Candidat</h2>
    <div v-if="quiz">
      <form @submit.prevent="submit">
        <div v-for="(q, idx) in quiz.questions" :key="idx" class="mb-4">
          <div class="font-semibold mb-2">{{ q.question }}</div>
          <div class="flex flex-col gap-2">
            <label v-for="(rep, i) in q.reponses" :key="i" class="flex items-center gap-2">
              <input type="radio" :name="'q_' + idx" :value="rep" v-model="reponses[idx]" />
              <span>{{ rep }}</span>
            </label>
          </div>
        </div>
        <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Envoyer mes
          réponses</button>
      </form>
      <div v-if="msg" class="mt-4 text-green-600">{{ msg }}</div>
      <div v-if="score !== null" class="mt-2 text-lg font-bold">Votre score : {{ score }} / {{ quiz.questions.length }}
      </div>
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
const score = ref(null)

onMounted(async () => {
  const token = route.params.token
  const res = await fetch(`http://localhost:8000/candidat/quiz/${token}`)
  if (res.ok) {
    quiz.value = await res.json()
  }
})

async function submit() {
  msg.value = ''
  score.value = null
  const token = route.params.token
  // Calcul du score côté front
  let sc = 0
  const allAnswers = []
  quiz.value.questions.forEach((q, idx) => {
    const rep = reponses.value[idx]
    allAnswers.push({ question: q.question, reponse: rep })
    if (rep && rep === q.reponse_correcte) sc++
  })
  score.value = sc
  // Envoie les réponses et le score au back
  const res = await fetch(`http://localhost:8000/candidat/quiz/${token}/repondre`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reponses: allAnswers, score: sc })
  })
  if (res.ok) {
    msg.value = 'Réponses envoyées !'
  }
}
</script>