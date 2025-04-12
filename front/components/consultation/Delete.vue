<script lang="ts" setup>
import type { Consultation } from '~/types'

const model = defineModel({
    type: Boolean
})

const props = defineProps({
    consultation: {
        type: Object as PropType<Consultation>,
        required: true,
    },
})

const emit = defineEmits(['delete'])
const toast = useToast()
const loading = ref(false)

const deleteConsultation = async () => {
    loading.value = true
    await apiRequest(
        () => $fetch(`/api/consultations/${props.consultation.id}/`, {
            method: 'DELETE',
            key: 'delete-consultation',
            credentials: "include"
        }),
        toast
    )
    toast.add({
        title: `Consultation avec ${props.consultation.patient.nom} ${props.consultation.patient.prenom}`,
        description: `Consultation supprimée avec succès`,
        color: 'success',
    })
    emit('delete', props.consultation.id)
    loading.value = false
    model.value = false
}

</script>
<template>
    <UModal v-model:open="model" :close="false" @close="model = false" title="Suppression" :color="'error'"
        :ui="{ title: 'text-red-500 dark:text-red-400' }" :icon="'i-heroicons-trash'"
        description="Vous êtes sur le point de supprimer la consultation avec" :loading="loading">
        <template #body>
            <p class="font-bold text-center mb-5">{{ props.consultation.patient.nom }} {{ props.consultation.patient.prenom }}</p>
            <div class="mt-2 border border-red-500 dark:border-red-400 rounded-md p-2 text-red-500 dark:text-red-400">
                <ul class="text-sm font-semibold">
                    <li>Tous les examens liés à cette consultation seront supprimés</li>
                    <li>Les résultats des examens ci-dessus seront supprimés également</li>
                    <li>Les prescriptions de la consultation seront supprimés</li>
                    <li>Cette action est irréversible</li>
                </ul>
            </div>
            <p class="mt-5">Êtes vous sûr de vouloir supprimer cette consultation ?</p>
            <div class="mt-8 flex justify-center items-center gap-8">
                <UButton label="Annuler" color="neutral" @click="model = false" />
                <UButton label="Supprimer" color="error" :loading="loading" @click="deleteConsultation" />
            </div>
        </template>
    </UModal>
</template>