<script lang="ts" setup>
import type { Patient } from '~/types'

const model = defineModel({
    type: Boolean
})

const props = defineProps({
    patient: {
        type: Object as PropType<Patient>,
        required: true,
    },
})

const emit = defineEmits(['delete'])
const toast = useToast()
const loading = ref(false)

const deletePatient = async () => {
    loading.value = true
    await apiRequest(
        () => $fetch(`/api/patients/${props.patient.id}/`, {
            method: 'DELETE',
            key: 'delete-patient',
            credentials: "include"
        }),
        toast
    )
    toast.add({
        title: `${props.patient.nom} ${props.patient.prenom}`,
        description: `Patient supprimé avec succès`,
        color: 'success',
    })
    emit('delete', props.patient.id)
    loading.value = false
    model.value = false
}

</script>
<template>
    <UModal v-model:open="model" :close="false" @close="model = false" title="Suppression" :color="'error'"
        :ui="{ title: 'text-red-500 dark:text-red-400' }" :icon="'i-heroicons-trash'"
        description="Vous êtes sur le point de supprimer le patient" :loading="loading">
        <template #body>
            <p class="font-bold text-center mb-5">{{ props.patient.nom }} {{ props.patient.prenom }}</p>
            <div class="mt-2 border border-red-500 dark:border-red-400 rounded-md p-2 text-red-500 dark:text-red-400">
                <ul class="text-sm font-semibold">
                    <li>Le dossier médical du patient sera supprimé</li>
                    <li>Les examens et les résultats du patient seront supprimés</li>
                    <li>Les prescriptions et traitements du patient seront supprimés</li>
                    <li>Cette action est irréversible</li>
                </ul>
            </div>
            <p class="mt-5">Êtes vous sûr de vouloir supprimer les données de ce patient ?</p>
            <div class="mt-8 flex justify-center items-center gap-8">
                <UButton label="Annuler" color="neutral" @click="model = false" />
                <UButton label="Supprimer" color="error" :loading="loading" @click="deletePatient" />
            </div>
        </template>
    </UModal>
</template>