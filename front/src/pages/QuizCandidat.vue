<template>
  <div class="max-w-3xl mx-auto p-6">
    <h2 class="text-2xl font-bold mb-8 text-center">Quiz Candidat</h2>

    <!-- Carousel des questions -->
    <div v-if="quiz && !showRecap" class="bg-white rounded-lg shadow-lg p-6">
      <div class="mb-6 flex flex-col justify-between items-center gap-4">
        <div class="text-sm text-gray-600">
          Question {{ currentQuestionIndex + 1 }} sur {{ quiz.questions.length }}
        </div>
        <div class="flex gap-2">
          <div v-for="(_, index) in quiz.questions" :key="index" :class="[
            'w-3 h-3 rounded-full',
            index === currentQuestionIndex ? 'bg-blue-600' :
              reponses[index] ? 'bg-green-500' : 'bg-gray-300'
          ]"></div>
        </div>
      </div>

      <div class="mb-8">
        <div class="font-semibold text-lg mb-4">{{ quiz.questions[currentQuestionIndex].question }}</div>
        <p class="text-gray-700 mb-6">{{ quiz.questions[currentQuestionIndex].texte }}</p>

        <div class="space-y-4">
          <label v-for="(rep, i) in quiz.questions[currentQuestionIndex].reponses" :key="i"
            class="flex items-center p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition"
            :class="{ 'border-blue-500 bg-blue-50': reponses[currentQuestionIndex] === rep }">
            <input type="radio" :name="'q_' + currentQuestionIndex" :value="rep"
              v-model="reponses[currentQuestionIndex]" class="mr-4" />
            <span>{{ rep.texte }}</span>
          </label>
        </div>
      </div>

      <div class="flex justify-between">
        <button v-if="currentQuestionIndex > 0" @click="currentQuestionIndex--"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition">
          Précédent
        </button>
        <div v-else class="w-24"></div>

        <button v-if="currentQuestionIndex < quiz.questions.length - 1" @click="nextQuestion"
          :disabled="!reponses[currentQuestionIndex]"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed">
          Suivant
        </button>
        <button v-else @click="showRecap = true" :disabled="!reponses[currentQuestionIndex]"
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed">
          Voir récapitulatif
        </button>
      </div>
    </div>

    <!-- Récapitulatif -->
    <div v-if="showRecap" class="bg-white rounded-lg shadow-lg p-6">
      <h3 class="text-xl font-bold mb-6">Récapitulatif de vos réponses</h3>

      <div v-for="(q, idx) in quiz.questions" :key="idx" class="mb-6 p-4 border rounded-lg">
        <div class="flex justify-between items-start mb-2">
          <div class="font-semibold">Question {{ idx + 1 }}</div>
          <button @click="modifierReponse(idx)" class="text-blue-600 hover:text-blue-800 text-sm">
            Modifier
          </button>
        </div>
        <p class="text-gray-700 mb-2 font-semibold">{{ q.texte }}</p>
        <div class="text-blue-600">
          Votre réponse : {{ reponses[idx]?.texte }}
        </div>
      </div>

      <div class="flex justify-between mt-8">
        <button @click="showRecap = false"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition">
          Retour aux questions
        </button>
        <button @click="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
          Soumettre le quiz
        </button>
      </div>
    </div>

    <div v-if="msg" class="mt-4 p-4 rounded-lg"
      :class="msg.includes('Erreur') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'">
      {{ msg }}
    </div>
    <div v-if="score !== null" class="mt-4 text-center text-lg font-bold">
      Votre score : {{ score }} / {{ quiz.questions.length }}
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
const currentQuestionIndex = ref(0)
const showRecap = ref(false)

onMounted(async () => {
  const token = route.params.token
  const res = await fetch(`http://localhost:8000/candidat/quiz/${token}`)
  if (res.ok) {
    quiz.value = await res.json()
    reponses.value = Array(quiz.value.questions.length).fill(null)
  }
  const res2 = await fetch(`http://localhost:8000/candidat/quiz/${token}/reponses`)
  if (res2.ok) {
    const data = await res2.json()
    if (data && data.length > 0) {
      dejaSoumis.value = true
      msg.value = 'Vous avez déjà répondu à ce quiz.'
    }
  }
})

function nextQuestion() {
  if (currentQuestionIndex.value < quiz.value.questions.length - 1) {
    currentQuestionIndex.value++
  }
}

function modifierReponse(index) {
  currentQuestionIndex.value = index
  showRecap.value = false
}

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