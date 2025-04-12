<script lang="ts" setup>
import { useUsersStore } from '~/store/userStore'

const model = defineModel({
    type: Boolean
})

const store = useUsersStore()
const loading = ref(false)

const logout = async () => {
    loading.value = true
    await store.logoutUser()
    loading.value = false
    model.value = false
    navigateTo('/login')
}

</script>

<template>
    <UModal v-model:open="model" :close="false" @close="model = false" title="Déconnexion" :color="'error'"
        :ui="{ title: 'text-red-500 dark:text-red-400' }" :icon="'i-heroicons-trash'"
        description="Vous serez redirigé vers la page de connexion" :loading="loading">
        <template #body>
            <p class="text-center">Voulez-vous vraiment vous déconnecter ?</p>
            <div class="mt-8 flex justify-center items-center gap-8">
                <UButton label="Non" color="neutral" @click="model = false" />
                <UButton label="Oui" icon="i-heroicons-arrow-right-start-on-rectangle-16-solid" 
                color="error" :loading="loading" @click="logout" />
            </div>
        </template>
    </UModal>
</template>