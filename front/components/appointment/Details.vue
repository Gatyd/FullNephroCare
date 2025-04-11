<script setup lang="ts">
import type { Appointment, Examen, Patient } from '~/types';

const props = defineProps({
    appointment: {
        type: Object as PropType<Appointment>,
        required: true
    },
})

const textModal = ref(false)
const completeLoading = ref(false)
const toast = useToast()
const emit = defineEmits(['edit', 'delete'])

const getHours = (date: Date) => {
    const options: Intl.DateTimeFormatOptions = { hour: "2-digit", minute: "2-digit" };
    return date.toLocaleString("fr-FR", options);
}

async function completer() {
    completeLoading.value = true
    const response = await apiRequest(
        () => $fetch(`/api/appointments/${props.appointment.id}/`, {
            method: 'PATCH',
            body: {
                statut: "COMPLETE",
            },
            credentials: "include",
        }),
        toast
    )
    if (response){
        toast.add({
            title: "Rendez-vous complété",
            description: `Le rendez-vous de ${(props.appointment.patient as Patient).prenom} ${(props.appointment.patient as Patient).nom} a été complété avec succès.`,
            color: "success",
        })
    }
    completeLoading.value = false
}

</script>
<template>
    <TextModal v-model="textModal" title="Notes de préparations" :body="appointment.notes_preparation"
        :description="`${(appointment.patient as Patient).prenom} ${(appointment.patient as Patient).nom}`" />
    <div class="p-5">
        <div class="flex justify-between">
            <div class="flex items-center gap-4">
                <div class="min-w-0">
                    <p class="text-gray-900 dark:text-white font-semibold">
                        {{ (appointment.patient as Patient).prenom }} {{ (appointment.patient as Patient).nom }}
                    </p>
                    <p class="text-gray-500 dark:text-gray-400 font-medium">
                        {{ appointment.motif }}
                    </p>
                </div>
            </div>

            <p class="font-medium text-gray-900 dark:text-white">
                {{ getHours(new Date(appointment.date_prevue)) }}
            </p>
        </div>
        <!--Patient details-->
        <div class="my-5 flex flex-col gap-4">
            <p v-if="(appointment.patient as Patient).email">Email: <em class="font-semibold">{{ (appointment.patient as
                Patient).email }}</em></p>
            <p>Téléphone: <em class="font-semibold">{{ (appointment.patient as Patient).telephone }}</em></p>
            <p class="whitespace-normal">
                Adresse: <em class="font-semibold break-words whitespace-pre-line">{{ (appointment.patient as
                    Patient).adresse
                }}</em>
            </p>
            <p>Stade MRC:
                <UBadge :color="getStadeColor((appointment.patient as Patient).stade_mrc)" variant="subtle" :label="(appointment.patient as Patient).stade_mrc ? `Stade ${(appointment.patient as Patient).stade_mrc}`
                    : 'Pas malade'" class="ms-3" />
            </p>
            <p>Débit de filtrage urinaire: <br> <em class="font-semibold">{{ (appointment.patient as Patient).dfu }} mL
                    / min / 1,73m²</em></p>

        </div>

        <!--Notes-->
        <div v-if="appointment.notes_preparation" class="my-5">
            <p>Notes de préparation:
                <UButton color="neutral" variant="subtle"
                    icon="i-heroicons-document-text" class="mx-10 my-1" 
                    @click="textModal = true"/>
            </p>
        </div>

        <!--Examen prealable details-->
        <div v-if="appointment.examen_prealable" class="my-5">
            <p>Examen préalable: <em class="font-semibold">{{ (appointment.examen_prealable as Examen).type_examen }}</em></p>
            <p>Date de réalisation: <em class="font-semibold">{{ formatDate((appointment.examen_prealable as Examen).date_realisation) }}</em></p>
        </div>

        <!--actions-->
        <div class="flex justify-around gap-4 mt-20">
            <UButton v-if="appointment.statut === 'PLANIFIE'" label="Compléter" color="success" 
            icon="i-heroicons-check-circle" @click="completer" :loading="completeLoading" />
            <UButton v-if="appointment.statut !== 'COMPLETE'" label="Reprogrammer" color="primary" 
            icon="i-heroicons-calendar-days" @click="$emit('edit', appointment)" />
            <UButton label="Supprimer" color="error" icon="i-heroicons-trash" @click="$emit('delete', appointment)" />
        </div>
    </div>
</template>