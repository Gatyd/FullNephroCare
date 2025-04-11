<script setup lang="ts">
const route = useRoute()
const id = route.params.id
const test = ref(0)
</script>

<template>
    <PatientSelectMenu v-model="test" />
    <p>ID du patient sélectionné: {{ test }}</p>
    <div class="h-full w-full flex items-center justify-center">
        <h1>PAGE SPECIFIQUE DU PATIENT {{ id }}</h1>
    </div>
</template>