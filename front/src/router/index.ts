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
import LiensCandidats from "../pages/LiensCandidats.vue";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/",
    component: () => import("../layouts/MainLayout.vue"),
    children: [
      {
        path: "dashboard",
        name: "Home",
        component: DashboardRH,
      },
      {
        path: "fiches",
        name: "Fiches",
        component: FichesPoste,
      },
      {
        path: "quiz",
        name: "Quiz",
        component: GenerateQuiz,
      },
      {
        path: "resultats",
        name: "Resultats",
        component: Resultats,
      },
      {
        path: "quiz-list",
        name: "QuizList",
        component: QuizList,
      },
      {
        path: "quiz/:id",
        name: "QuizDetail",
        component: QuizDetail,
      },
      {
        path: "candidat/quiz/:token",
        name: "QuizCandidat",
        component: QuizCandidat,
      },
      {
        path: "liens-candidats",
        name: "LiensCandidats",
        component: LiensCandidats,
      },
    ],
  },
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