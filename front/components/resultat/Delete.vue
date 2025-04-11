<script lang="ts" setup>
import type { ResultatExamen } from '~/types'

const model = defineModel({
    type: Boolean
})

const props = defineProps({
    resultat: {
        type: Object as PropType<ResultatExamen>,
        required: true,
    },
})

const emit = defineEmits(['delete'])
const toast = useToast()
const loading = ref(false)

const deleteResultat = async () => {
    loading.value = true
    try {
    await apiRequest(
        () => $fetch(`/api/resultats-examens/${props.resultat.id}/`, {
        method: 'DELETE',
        key: 'delete-resultat',
        credentials: "include"
        }),
        toast
    );

    toast.add({
        title: 'Suppression du résultat',
        description: 'Résultat supprimé avec succès',
        color: 'success',
    });
    } catch (error) {
    console.error('Erreur lors de la suppression :', error);
    toast.add({
        title: 'Erreur',
        description: 'Échec de la suppression de l\'examen',
        color: 'error',
    });
    }

    emit('delete', props.resultat.id)
    loading.value = false
    model.value = false
}

</script>
<template>
    <UModal v-model:open="model" :close="false" @close="model = false" title="Suppression" :color="'error'"
        :ui="{ title: 'text-red-500 dark:text-red-400' }" :icon="'i-heroicons-trash'"
        description="Vous êtes sur le point de supprimer l'examen" :loading="loading">
        <template #body>
            <div class="mt-2 border border-red-500 dark:border-red-400 rounded-md p-2 text-red-500 dark:text-red-400">
                <p class="text-lg mb-4">Êtes-vous sûr de vouloir supprimer le résultat </p>
                <p class="text-sm text-gray-500">Cette action est irréversible.</p>
            </div>
            <div class="mt-8 flex justify-center items-center gap-8">
                <UButton label="Annuler" color="neutral" @click="model = false" />
                <UButton label="Supprimer" color="error" :loading="loading" @click="deleteResultat" />
            </div>
        </template>
    </UModal>
</template>