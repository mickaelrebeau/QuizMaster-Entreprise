<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Quiz Candidat</h2>
    <div v-if="quiz" class="bg-white rounded-lg shadow p-6 flex flex-col">
      <form @submit.prevent="submit">
        <div v-for="(q, idx) in quiz.questions" :key="idx" class="mb-4">
          <div class="font-semibold mb-2">{{ q.question }}</div>
          <div class="flex flex-col gap-2">
            <p class="font-semibold text-left mb-4">{{ q.texte }}</p>
            <label v-for="(rep, i) in q.reponses" :key="i" class="flex items-center gap-4">
              <input type="radio" :name="'q_' + idx" :value="rep" v-model="reponses[idx]" />
              <span>{{ rep.texte }}</span>
            </label>
          </div>
        </div>
        <button class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          :disabled="dejaSoumis">Envoyer mes
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
const reponses = ref([])
const msg = ref('')
const score = ref(null)
const dejaSoumis = ref(false)

onMounted(async () => {
  const token = route.params.token
  const res = await fetch(`http://localhost:8000/candidat/quiz/${token}`)
  if (res.ok) {
    quiz.value = await res.json()
    reponses.value = Array(quiz.value.questions.length).fill(null)
  }
  // Vérifie si le quiz a déjà été soumis
  const res2 = await fetch(`http://localhost:8000/candidat/quiz/${token}/reponses`)
  if (res2.ok) {
    const data = await res2.json()
    if (data && data.length > 0) {
      dejaSoumis.value = true
      msg.value = 'Vous avez déjà répondu à ce quiz.'
    }
  }
})

async function submit() {
  msg.value = ''
  score.value = null
  const token = route.params.token

  if (reponses.value.some(r => !r)) {
    msg.value = 'Merci de répondre à toutes les questions avant de valider !'
    return
  }

  let sc = 0
  const allAnswers = []
  quiz.value.questions.forEach((q, idx) => {
    const rep = reponses.value[idx]
    allAnswers.push({ question: q.texte, reponse: rep ? rep.texte : null })
    if (rep && rep.is_correct) sc++
  })
  score.value = sc
  // Envoie les réponses et le score au back
  try {
    const res = await fetch(`http://localhost:8000/candidat/quiz/${token}/repondre`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reponses: allAnswers, score: sc })
    })
    if (res.ok) {
      msg.value = 'Réponses envoyées !'
      dejaSoumis.value = true
    } else {
      const data = await res.json()
      if (data.detail && data.detail.includes('déjà répondu')) {
        msg.value = data.detail
        dejaSoumis.value = true
      } else {
        msg.value = 'Erreur lors de la soumission.'
      }
    }
  } catch (e) {
    msg.value = 'Erreur réseau.'
  }
}
</script>