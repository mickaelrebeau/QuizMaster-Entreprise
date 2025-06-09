<template>
    <header class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <router-link to="/dashboard"
                        class="text-xl font-bold bg-gradient-to-r from-blue-600 to-emerald-500 bg-clip-text text-transparent">
                        QuizMaster Entreprise
                    </router-link>
                </div>
                <nav class="hidden md:flex items-center space-x-8">
                    <router-link to="/fiches" class="text-gray-600 hover:text-gray-900 transition-colors duration-200 flex flex-col items-center active:text-blue-600">
                        <i class="fas fa-file-alt mr-2"></i>
                        Fiches de poste
                    </router-link>
                    <router-link to="/quiz" class="text-gray-600 hover:text-gray-900 transition-colors duration-200 flex flex-col items-center active:text-blue-600">
                        <i class="fas fa-brain mr-2"></i>
                        Générer un quiz
                    </router-link>
                    <router-link to="/quiz-list" class="text-gray-600 hover:text-gray-900 transition-colors duration-200 flex flex-col items-center active:text-blue-600">
                        <i class="fas fa-list mr-2"></i>
                        Liste des quiz
                    </router-link>
                    <router-link to="/resultats" class="text-gray-600 hover:text-gray-900 transition-colors duration-200 flex flex-col items-center active:text-blue-600">
                        <i class="fas fa-chart-bar mr-2"></i>
                        Résultats
                    </router-link>
                    <router-link to="/liens-candidats" class="text-gray-600 hover:text-gray-900 transition-colors duration-200 flex flex-col items-center active:text-blue-600">
                        <i class="fas fa-link mr-2"></i>
                        Liens candidats
                    </router-link>
                    <button @click="logout" class="btn-secondary">
                        <i class="fas fa-sign-out-alt mr-2"></i>
                        Déconnexion
                    </button>
                </nav>
                <div class="md:hidden">
                    <button @click="toggleMobileMenu" class="text-gray-500 hover:text-gray-700">
                        <i class="fas fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Menu mobile -->
        <div v-if="isMobileMenuOpen" class="md:hidden bg-white border-t border-gray-100">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <router-link to="/dashboard" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center">
                    <i class="fas fa-home mr-2"></i>
                    Accueil
                </router-link>
                <router-link to="/fiches" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center">
                    <i class="fas fa-file-alt mr-2"></i>
                    Fiches de poste
                </router-link>
                <router-link to="/quiz" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center">
                    <i class="fas fa-brain mr-2"></i>
                    Générer un quiz
                </router-link>
                <router-link to="/quiz-list" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center">
                    <i class="fas fa-list mr-2"></i>
                    Liste des quiz
                </router-link>
                <router-link to="/resultats" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center">
                    <i class="fas fa-chart-bar mr-2"></i>
                    Résultats
                </router-link>
                <router-link to="/liens-candidats" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center">
                    <i class="fas fa-link mr-2"></i>
                    Liens candidats
                </router-link>
                <button @click="logout" class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200 flex items-center w-full text-left">
                    <i class="fas fa-sign-out-alt mr-2"></i>
                    Déconnexion
                </button>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isMobileMenuOpen = ref(false)

function toggleMobileMenu() {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function logout() {
    localStorage.removeItem('token')
    router.push('/login')
}
</script>