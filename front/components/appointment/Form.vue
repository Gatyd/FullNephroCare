<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui';
import type { Appointment, Patient } from '~/types';

const props = defineProps({
    appointment: {
        type: Object as PropType<Appointment>,
        required: false,
    },
    date: {
        type: String,
        required: false,
    },
})
const model = defineModel({
    type: Boolean
})
const emit = defineEmits(['create', 'update'])
const loading = ref(false)
const toast = useToast()

const state = reactive({
    patient: 0,
    date_prevue: "",
    time: "",
    motif: "",
    notes_preparation: "",
})

if (props.date) {
    state.date_prevue = props.date
}

const validate = (state: any): FormError[] => {
    const errors = []
    if (!state.patient) errors.push({ name: 'patient', message: 'Veuillez sélectionner un patient' })
    if (props.date) {
        if (!state.time) errors.push({ name: 'time', message: 'Veuillez entrer l\'heure prévue' })
        else if (new Date(`${state.date_prevue}T${state.time}`) < new Date()) {
            errors.push({ name: 'time', message: 'L\'heure prévue ne peut pas être dans le passé' })
        }
    } else {
        if (!state.date_prevue) errors.push({ name: 'date_prevue', message: 'Veuillez entrer la date prévue' })
        else if (new Date(state.date_prevue) < new Date()) {
            errors.push({ name: 'date_prevue', message: 'La date prévue ne peut pas être dans le passé' })
        }
    }
    if (!state.motif) errors.push({ name: 'motif', message: 'Veuillez entrer le motif' })
    console.log('errors', errors)
    return errors
}

function resetForm() {
    state.patient = 0
    state.date_prevue = ""
    state.motif = ""
    state.notes_preparation = ""
}

watch(() => model.value, () => {
    if (props.appointment) {
        state.patient = (props.appointment.patient as Patient).id
        state.date_prevue = props.appointment.date_prevue
        state.motif = props.appointment.motif
        state.notes_preparation = props.appointment.notes_preparation || ""
    } else {
        resetForm()
    }
})

async function onSubmit(event: FormSubmitEvent<any>) {
    loading.value = true
    const body = event.data
    if (props.date) {
        body.date_prevue = `${state.date_prevue} ${state.time}`
    } else {
        body.date_prevue = state.date_prevue
    }
    body['notes_preparation'] = body.notes_preparation === "" ? null : body.notes_preparation
    const res = await apiRequest<Appointment>(
        () => $fetch(`/api/appointments/${props.appointment ? `${props.appointment.id}/` : ''}`, {
            method: props.appointment ? "PATCH" : "POST",
            body: body,
            credentials: "include"
        }),
        toast
    );
    console.log('res', res)
    if (res) {
        emit(props.appointment ? 'update' : 'create', res)
        toast.add({
            title: formatDate(res.date_prevue,),
            description: `Rendez-vous avec ${(res.patient as Patient).nom.split(' ')[0]} 
            ${(res.patient as Patient).prenom.split(' ')[0]} ${props.appointment ? 'modifié' : 'créé'} avec succès`,
            color: "success",
            icon: "i-heroicons-check-circle",
            duration: 3000,
        })
        resetForm()
        model.value = false
    }
    loading.value = false
}

</script>
<template>
    <UModal v-model:open="model" :title="`${appointment ? 'Reprogrammer' : 'Ajouter'} un rendez-vous`"
        :description="`${appointment ? 'Mettez à jour' : 'Remplissez'} les informations du rendez-vous`">
        <template #body>
            <UForm :state="state" :validate="validate" @submit="onSubmit" class="flex flex-col gap-4">
                <PatientSelectMenu v-if="!appointment" v-model="state.patient" />
                <UFormField v-if="!date" label="Date et heure prévue" name="date_prevue" required>
                    <UInput v-model="state.date_prevue" type="datetime-local" placeholder="Sélectionner une date"
                        class="w-full" />
                </UFormField>
                <UFormField v-else label="Heure prévue" name="heure_prevue" required>
                    <UInput v-model="state.time" type="time" placeholder="Sélectionnez une heure" class="w-full" />
                </UFormField>
                <UFormField label="Motif" name="motif" required>
                    <UInput v-model="state.motif" class="w-full" />
                </UFormField>
                <UFormField label="Notes de préparation" name="notes_preparation">
                    <UTextarea v-model="state.notes_preparation" :rows="5" class="w-full" />
                </UFormField>

                <div class="mt-8 flex justify-end items-center gap-8">
                    <UButton label="Annuler" color="neutral" @click="model = false" />
                    <UButton :label="appointment ? 'Modifier' : 'Enregistrer'" :loading="loading" type="submit"
                        :color="appointment ? 'primary' : 'success'" />
                </div>
            </UForm>
        </template>
    </UModal>
</template>