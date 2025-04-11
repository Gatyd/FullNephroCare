<script lang="ts" setup>
import type { Appointment, Patient } from '~/types'

const model = defineModel({
    type: Boolean
})

const props = defineProps({
    appointment: {
        type: Object as PropType<Appointment>,
        required: true,
    },
})

const emit = defineEmits(['delete'])
const toast = useToast()
const loading = ref(false)

const deleteAppointment = async () => {
    loading.value = true
    await apiRequest(
        () => $fetch(`/api/appointments/${props.appointment.id}/`, {
            method: 'DELETE',
            credentials: "include"
        }),
        toast
    )
    toast.add({
        title: `${(props.appointment.patient as Patient).prenom} ${(props.appointment.patient as Patient).nom}`,
        description: `Rendez-vous supprimé avec succès`,
        color: 'success',
    })
    emit('delete', props.appointment.id)
    loading.value = false
    model.value = false
}

</script>
<template>
    <UModal v-model:open="model" :close="false" @close="model = false" title="Suppression de rendez-vous" :color="'error'"
        :ui="{ title: 'text-red-500 dark:text-red-400' }" :icon="'i-heroicons-trash'"
        description="Vous êtes sur le point de supprimer un rendez-vous" :loading="loading">
        <template #body>
            <p class="font-bold text-center mb-5">{{ (props.appointment.patient as Patient).nom }} {{ (props.appointment.patient as Patient).prenom }}</p>
            <p class="mt-5">Êtes vous sûr de vouloir supprimer ce rendez-vous ?</p>
            <div class="mt-8 flex justify-center items-center gap-8">
                <UButton label="Annuler" color="neutral" @click="model = false" />
                <UButton label="Supprimer" color="error" :loading="loading" @click="deleteAppointment" />
            </div>
        </template>
    </UModal>
</template>