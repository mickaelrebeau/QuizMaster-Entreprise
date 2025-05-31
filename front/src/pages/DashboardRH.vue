<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold mb-6">Tableau de bord RH</h1>
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
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Évolution des quiz générés (12 derniers mois)</h2>
          <Line :data="lineData" :options="lineOptions" />
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Distribution des scores</h2>
          <Pie :data="pieData" :options="pieOptions" />
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6 mt-8 max-w-md mx-auto">
        <h2 class="text-lg font-semibold mb-4">Taux de complétion des quiz</h2>
        <Doughnut :data="doughnutData" :options="doughnutOptions" />
        <div class="text-center mt-4 text-xl font-bold">
          {{ tauxCompletion }}%
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
      text: 'Vue d’ensemble des quiz et résultats'
    }
  }
}

// Line chart (quiz par mois)
const lineData = ref({
  labels: [],
  datasets: [
    {
      label: 'Quiz générés',
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
    // Quiz par mois
    const resLine = await fetch('http://localhost:8000/stats/quizzes-per-month')
    const dataLine = await resLine.json()
    lineData.value.labels = dataLine.map(item => item[0])
    lineData.value.datasets[0].data = dataLine.map(item => item[1])
    // Distribution des scores
    const resPie = await fetch('http://localhost:8000/stats/score-distribution')
    const dataPie = await resPie.json()
    pieData.value.labels = dataPie.map(item => item.range)
    pieData.value.datasets[0].data = dataPie.map(item => item.count)
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