<template>
    <Teleport to="body">
        <div v-if="modelValue" class="fixed inset-0 z-[9999]">
            <!-- Overlay -->
            <div class="fixed inset-0 bg-black/50" @click="$emit('update:modelValue', false)"></div>

            <!-- Modal -->
            <div class="fixed inset-0 flex items-center justify-center p-4">
                <div class="bg-white rounded-lg shadow-xl w-full max-w-md transform transition-all">
                    <!-- Header -->
                    <div class="flex justify-between items-center p-4 border-b">
                        <h3 class="text-lg font-bold">{{ title }}</h3>
                        <button @click="$emit('update:modelValue', false)" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>

                    <!-- Content -->
                    <div class="p-4">
                        <slot></slot>
                    </div>

                    <!-- Footer -->
                    <div v-if="$slots.footer" class="p-4 border-t">
                        <slot name="footer"></slot>
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
    title: {
        type: String,
        default: ''
    }
})

defineEmits(['update:modelValue'])
</script>