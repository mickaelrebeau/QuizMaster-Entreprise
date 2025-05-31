<template>
    <v-layout>
        <v-app-bar app class="px-10">
            <div class="d-flex align-center justify-center w-full">
                <span style="color: #eceff1" class="app-bar-text mx-3 text-h5 font-bold">
                    QuizMaster Entreprise
                </span>
            </div>
        </v-app-bar>

        <v-main>
            <router-view />
        </v-main>
    </v-layout>
</template>

<script setup>
</script>