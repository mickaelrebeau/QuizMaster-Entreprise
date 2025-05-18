// @ts-nocheck
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import DashboardRH from '../pages/DashboardRH.vue'
import FichesPoste from '../pages/FichesPoste.vue'
import GenerateQuiz from '../pages/GenerateQuiz.vue'
import Resultats from '../pages/Resultats.vue'
import QuizCandidat from '../pages/QuizCandidat.vue'
import Register from '../pages/Register.vue'
import QuizList from "../pages/QuizList.vue";
import QuizDetail from "../pages/QuizDetail.vue";

const routes = [
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/dashboard", component: DashboardRH },
  { path: "/fiches", component: FichesPoste },
  { path: "/quiz", component: GenerateQuiz },
  { path: "/resultats", component: Resultats },
  { path: "/quiz-list", component: QuizList },
  { path: "/quiz/:id", component: QuizDetail },
  { path: "/candidat/quiz/:token", component: QuizCandidat },
  { path: "/", redirect: "/login" },
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard pour protéger les routes RH
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path.startsWith('/dashboard') || ['/fiches','/quiz','/resultats'].includes(to.path)) {
    if (!token) {
      return next('/login')
    }
  }
  if (to.path === '/login' && token) {
    return next('/dashboard')
  }
  next()
})

export default router 