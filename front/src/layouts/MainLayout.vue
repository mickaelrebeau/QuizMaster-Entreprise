<template>
    <div class="min-h-screen bg-gray-50">
        <Header />
        <main class="main-content pt-20">
            <div class="fade-in">
                <router-view v-slot="{ Component }">
                    <transition name="fade" mode="out-in">
                        <component :is="Component" />
                    </transition>
                </router-view>
            </div>
        </main>
    </div>
</template>

<script setup>
import Header from '../components/Header.vue';
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
.main-content {
    animation: fadeIn 0.5s ease-out;
}
</style>