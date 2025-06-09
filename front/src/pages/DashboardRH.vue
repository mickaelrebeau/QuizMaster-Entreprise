<template>
  <div class="p-8">
    <h1 class="text-xl font-bold mb-6">Tableau de bord RH</h1>
    <div v-if="loading" class="text-gray-500">Chargement...</div>
    <div v-else>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-bold">{{ stats.nb_quiz }}</span>
          <span class="text-gray-600 mt-2">Quiz générés</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-bold">{{ stats.nb_liens }}</span>
          <span class="text-gray-600 mt-2">Liens générés</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-bold">{{ stats.nb_resultats_recus }}</span>
          <span class="text-gray-600 mt-2">Résultats reçus</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-bold">{{ stats.nb_resultats_en_attente }}</span>
          <span class="text-gray-600 mt-2">Résultats en attente</span>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6 my-8">
        <Bar :data="chartData" :options="chartOptions" />
      </div>

      <div class="bg-white rounded-lg shadow p-6 my-8 flex flex-col justify-between items-center">
        <h2 class="text-lg font-semibold">Évolution des données</h2>
        <div class="flex gap-4">
          <select v-model="selectedType" @change="updateLineChart" class="px-2 py-1 border rounded">
            <option value="quiz">Quiz générés</option>
            <option value="score">Moyenne des scores</option>
            <option value="liens">Liens générés</option>
            <option value="completion">Taux de complétion</option>
          </select>
          <select v-model="selectedMonths" @change="updateLineChart" class="px-2 py-1 border rounded">
            <option value="3">3 derniers mois</option>
            <option value="6">6 derniers mois</option>
            <option value="12">12 derniers mois</option>
            <option value="24">24 derniers mois</option>
          </select>
        </div>
        <Line :data="lineData" :options="lineOptions" />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Distribution des scores</h2>
          <Pie :data="pieData" :options="pieOptions" />
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Taux de complétion des quiz</h2>
          <Doughnut :data="doughnutData" :options="doughnutOptions" />
          <div class="text-center mt-4 text-xl font-bold">
            {{ tauxCompletion }}%
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Bar, Line, Pie, Doughnut } from 'vue-chartjs'
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Title, Tooltip, Legend)

const stats = ref({
  nb_quiz: 0,
  nb_liens: 0,
  nb_resultats_recus: 0,
  nb_resultats_en_attente: 0
})
const loading = ref(true)
const selectedType = ref('quiz')
const selectedMonths = ref('12')

// Bar chart (overview)
const chartData = ref({
  labels: [
    'Quiz générés',
    'Liens générés',
    'Résultats reçus',
    'Résultats en attente'
  ],
  datasets: [
    {
      label: 'Statistiques',
      backgroundColor: [
        '#3b82f6',
        '#10b981',
        '#f59e42',
        '#ef4444'
      ],
      data: [0, 0, 0, 0]
    }
  ]
})
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: {
      display: true,
      text: "Vue d'ensemble des quiz et résultats"
    }
  }
}

// Line chart (évolution)
const lineData = ref({
  labels: [],
  datasets: [
    {
      label: 'Évolution',
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.2)',
      data: []
    }
  ]
})
const lineOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

// Pie chart (distribution des scores)
const pieData = ref({
  labels: [],
  datasets: [
    {
      label: 'Distribution des scores',
      backgroundColor: [
        '#3b82f6',
        '#10b981',
        '#f59e42',
        '#ef4444'
      ],
      data: []
    }
  ]
})
const pieOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    title: {
      display: false
    }
  }
}

// Doughnut chart (taux de complétion)
const doughnutData = ref({
  labels: ['Complétés', 'En attente'],
  datasets: [
    {
      backgroundColor: ['#10b981', '#f59e42'],
      data: [0, 0]
    }
  ]
})
const doughnutOptions = {
  cutout: '70%',
  plugins: {
    legend: { display: false },
    title: { display: false }
  }
}

const tauxCompletion = computed(() => {
  const total = stats.value.nb_liens
  const done = stats.value.nb_resultats_recus
  if (!total) return 0
  return Math.round((done / total) * 100)
})

async function updateLineChart() {
  try {
    const res = await fetch(`http://localhost:8000/stats/evolution?type_data=${selectedType.value}&months=${selectedMonths.value}`)
    if (res.ok) {
      const data = await res.json()

      // Formatage des dates en français
      const mois = ['Jan.', 'Fév.', 'Mar.', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Août', 'Sep.', 'Oct.', 'Nov.', 'Déc.']
      lineData.value.labels = data.map(item => {
        const date = new Date(item.month)
        return `${mois[date.getMonth()]} ${date.getFullYear()}`
      })
      lineData.value.datasets[0].data = data.map(item => item.value)

      // Mise à jour du label en fonction du type de données
      const labels = {
        quiz: 'Nombre de quiz générés',
        score: 'Moyenne des scores',
        liens: 'Nombre de liens générés',
        completion: 'Taux de complétion (%)'
      }
      lineData.value.datasets[0].label = labels[selectedType.value]
    }
  } catch (e) {
    console.error('Erreur lors de la mise à jour du graphique:', e)
  }
}

onMounted(async () => {
  try {
    // Stats globales
    const res = await fetch('http://localhost:8000/stats')
    const data = await res.json()
    stats.value = data
    chartData.value.datasets[0].data = [
      data.nb_quiz,
      data.nb_liens,
      data.nb_resultats_recus,
      data.nb_resultats_en_attente
    ]
    doughnutData.value.datasets[0].data = [
      data.nb_resultats_recus,
      data.nb_resultats_en_attente
    ]

    // Distribution des scores
    const resPie = await fetch('http://localhost:8000/stats/score-distribution')
    const dataPie = await resPie.json()
    pieData.value.labels = dataPie.map(item => item.range)
    pieData.value.datasets[0].data = dataPie.map(item => item.count)

    // Évolution initiale
    await updateLineChart()
  } catch (e) {
    alert('Erreur lors du chargement des statistiques')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
body {
  background: #f3f4f6;
}
</style>