<script setup lang="ts">
const model = defineModel({
    type: Boolean
})
const props = defineProps({
    title: {
        type: String
    },
    body: {
        type: String,
    },
    description: {
        type: String,
    },
})

</script>
<template>
    <UModal v-model:open="model" :title="title" :description="description">
        <template #body>
            <div class="p-4">
                <p class="text-center">
                    {{ body }}
                </p>
            </div>
        </template>
    </UModal>
</template>