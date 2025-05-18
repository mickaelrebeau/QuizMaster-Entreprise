<template>
    <header class="fixed top-3 left-1/2 -translate-x-1/2 mx-auto max-w-6xl w-full z-50 bg-gray-800 text-white px-8 py-4 flex items-center justify-between shadow rounded-full">
        <div class="text-xl font-bold">QuizMaster Entreprise</div>
        <nav class="flex items-center gap-4">
            <router-link to="/">
                <p class="text-white hover:text-gray-300">Accueil</p>
            </router-link>
            <router-link to="/fiches" class="hover:underline">
                <p class="text-white hover:text-gray-300">Fiches de poste</p>
            </router-link>
            <router-link to="/quiz" class="hover:underline">
                <p class="text-white hover:text-gray-300">Générer un quiz</p>
            </router-link>
            <router-link to="/quiz-list" class="hover:underline">
                <p class="text-white hover:text-gray-300">Liste des quiz</p>
            </router-link>
            <router-link to="/resultats" class="hover:underline">
                <p class="text-white hover:text-gray-300">Résultats</p>
            </router-link>
            <button @click="logout" class="text-white hover:text-gray-300">
                <p>Déconnexion</p>
            </button>
        </nav>
    </header>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
    localStorage.removeItem('token')
    router.push('/login')
}
</script>