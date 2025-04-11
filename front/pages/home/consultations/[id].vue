<script setup lang="ts">
const route = useRoute()
const id = route.params.id
</script>

<template>
    <div class="h-full w-full flex items-center justify-center">
        <h1>DETAILS DE LA CONSULTATION {{ id }}</h1>
    </div>
</template>