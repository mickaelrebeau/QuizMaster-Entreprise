<template>
    <Teleport to="body">
        <div v-if="modelValue" class="fixed inset-0 z-[9999]">
            <!-- Overlay -->
            <div class="fixed inset-0 bg-black/50" @click="$emit('update:modelValue', false)"></div>

            <!-- Modal -->
            <div class="fixed inset-0 flex items-center justify-center p-4">
                <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl transform transition-all">
                    <!-- Header -->
                    <div class="flex justify-between items-center p-4 border-b">
                        <h3 class="text-lg font-bold">Réponses détaillées du candidat</h3>
                        <button @click="$emit('update:modelValue', false)" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>

                    <!-- Content -->
                    <div class="p-4 max-h-[70vh] overflow-y-auto">
                        <ul class="space-y-4">
                            <li v-for="(rep, idx) in reponses" :key="idx"
                                class="p-4 border rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                                <div class="font-semibold text-gray-800 mb-2">Question {{ idx + 1 }} : {{ rep.question
                                    }}</div>
                                <div class="space-y-2">
                                    <div :class="[
                                        'p-2 rounded',
                                        rep.reponse_choisie === rep.bonne_reponse
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-red-100 text-red-800'
                                    ]">
                                        <span class="font-medium">Votre réponse :</span> {{ rep.reponse_choisie }}
                                    </div>
                                    <div v-if="rep.bonne_reponse && rep.reponse_choisie !== rep.bonne_reponse"
                                        class="p-2 rounded bg-green-100 text-green-800">
                                        <span class="font-medium">Bonne réponse :</span> {{ rep.bonne_reponse }}
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>

                    <!-- Footer -->
                    <div class="p-4 border-t">
                        <button @click="$emit('update:modelValue', false)"
                            class="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    reponses: {
        type: Array,
        required: true
    }
})

defineEmits(['update:modelValue'])
</script>