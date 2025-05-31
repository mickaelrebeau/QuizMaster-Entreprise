<template>
    <v-layout>
        <Header />

        <v-main class="main-content">
            <router-view />
        </v-main>
    </v-layout>
</template>

<script setup>
import Header from '../components/Header.vue';
</script>

<style scoped>
.main-content {
    min-height: calc(100vh - 128px);
    padding: 20px;
}
</style>