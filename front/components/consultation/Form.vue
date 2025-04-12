<script lang="ts" setup>
import type { Consultation, Patient } from '~/types';
import type { FormError, FormSubmitEvent } from '@nuxt/ui'

const props = defineProps({
    consultation: {
        type: Object as PropType<Consultation>,
        required: false,
    },
})

const model = defineModel({
    type: Boolean
})
const emit = defineEmits(['create', 'update'])
const toast = useToast()
const createLoading = ref(false)
const updateLoading = ref(false)
const currentForm = ref(0)

const typeConsultationOptions = [
    { value: 'INITIALE', label: 'Consultation initiale' },
    { value: 'SUIVI', label: 'Consultation de suivi' },
    { value: 'URGENCE', label: 'Consultation d\'urgence' }
]

const consultationState = reactive({
    patient: 0,
    type_consultation: "INITIALE",
    symptomes: "M",
    diagnostic: "",
})

const examenState = reactive({
    type_examen: "",
    description: "",
    date_realisation: "",
    urgence: false,
})

watch(() => model.value, () => {
    if (props.consultation) {
        const consultation = props.consultation
        consultationState.patient = consultation.patient.id
        consultationState.type_consultation = consultation.type_consultation
        consultationState.symptomes = consultation.symptomes
        consultationState.diagnostic = consultation.diagnostic
    } else {
        resetForm()
    }
})

const updateValidated = (state: any): FormError[] => {
    const errors = []
    if (!state.patient) errors.push({ name: 'patient', message: 'Veuillez entrer le patient' })
    if (!state.type_consultation) errors.push({ name: 'type_consultation', message: 'Veuillez entrer le type de consultation' })
    if (!state.symptomes) errors.push({ name: 'symptomes', message: 'Veuillez entrer les symptômes' })
    return errors
}

const examenValidated = (state: any): FormError[] => {
    const errors = []
    if (!state.type_examen) errors.push({ name: 'type_examen', message: 'Veuillez entrer le type d\'examen' })
    if (!state.date_realisation) errors.push({ name: 'date_realisation', message: 'Veuillez entrer la date de réalisation' })
    else if (new Date(state.date_realisation) < new Date()) {
        errors.push({ name: 'date_realisation', message: 'La date de réalisation ne peut pas être dans le passé' })
    }
    return errors
}

function resetForm() {
    consultationState.patient = 0
    consultationState.type_consultation = "INITIALE"
    consultationState.symptomes = ""
    consultationState.diagnostic = ""
    examenState.type_examen = ""
    examenState.description = ""
    examenState.date_realisation = ""
    examenState.urgence = false
}

async function onConsultationSubmit() {
    if (props.consultation) {
        updateLoading.value = true
        const res = await apiRequest<Consultation>(
            () => $fetch(`/api/consultations/${props.consultation?.id}/`, {
                method: "PATCH",
                body: {
                    ...consultationState,
                },
                credentials: "include"
            }),
            toast
        );
        if (res) {
            emit('update', res)
            toast.add({
                title: `Consultation avec ${res.patient.prenom} ${res.patient.nom}`,
                description: `Consultation modifié avec succès`,
                color: "success",
                icon: "i-heroicons-check-circle",
                duration: 3000,
            })
            resetForm()
            model.value = false
        }
        updateLoading.value = false
    } else {
        currentForm.value = 1
    }
}

async function onSubmit(event: FormSubmitEvent<any>) {
    createLoading.value = true
    const res = await apiRequest<Consultation>(
        () => $fetch(`/api/consultations/`, {
            method: "POST",
            body: {
                ...consultationState,
                examen: {
                    patient: consultationState.patient,
                    type_examen: examenState.type_examen,
                    description: examenState.description,
                    date_realisation: examenState.date_realisation,
                    urgence: examenState.urgence,
                }
            },
            credentials: "include"
        }),
        toast
    );
    if (res) {
        emit('create', res)
        toast.add({
            title: `Consultation avec ${res.patient.prenom} ${res.patient.nom}`,
            description: `Consultation ${props.consultation ? 'modifié' : 'créé'} avec succès`,
            color: "success",
            icon: "i-heroicons-check-circle",
            duration: 3000,
        })
        resetForm()
        model.value = false
    }
    createLoading.value = false
}

</script>
<template>
    <UModal v-model:open="model" :title="`${consultation ? 'Modifier' : 'Faire'} une consultation`"
        :description="`${consultation ? 'Mettez à jour' : 'Remplissez'} les informations de la consultation`"
        :ui="{ content: 'max-w-2xl' }">
        <template #body>
            <UForm v-if="currentForm === 0" :validate="updateValidated" :state="consultationState"
                @submit="onConsultationSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <PatientSelectMenu v-model="consultationState.patient" class="col-span-1" />
                <UFormField class="col-span-1" name="type_consultation" label="Type de consultation" :required="true">
                    <USelect v-model="consultationState.type_consultation" :items="typeConsultationOptions"
                        class="w-full" value-key="value" label-key="label" />
                </UFormField>
                <UFormField class="col-span-1" name="symptomes" label="Symptômes" :required="true">
                    <UTextarea v-model="consultationState.symptomes" :rows="5" class="w-full" />
                </UFormField>
                <UFormField class="col-span-1" name="diagnostic" label="Diagnostic">
                    <UTextarea v-model="consultationState.diagnostic" :rows="5" class="w-full" />
                </UFormField>
                <div class="col-span-2 flex justify-end items-center px-2 mt-5 gap-4">
                    <UButton @click="model = false" color="neutral" label="Annuler" />
                    <UButton type="submit" :loading="updateLoading" :color="consultation ? 'primary' : 'success'"
                        :label="consultation ? 'Modifier' : 'Suivant'" />
                </div>
            </UForm>
            <UForm v-else-if="currentForm === 1" :validate="examenValidated" :state="examenState" @submit="onSubmit"
                class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <UFormField name="type_examen" label="Type d'examen" :required="true" class="col-span-1">
                    <UInput v-model="examenState.type_examen" type="text" class="w-full" />
                </UFormField>
                <UFormField name="date_realisation" label="Date de réalisation" :required="true" class="col-span-1">
                    <UInput v-model="examenState.date_realisation" type="datetime-local" class="w-full" />
                </UFormField>
                <UFormField name="description" label="Description de l'examen" class="col-span-2">
                    <UTextarea v-model="examenState.description" :rows="5" class="w-full" />
                </UFormField>
                <UFormField class="col-span-2 my-1" name="urgence" required>
                    <UCheckbox v-model="examenState.urgence" class="w-full " label="Urgent" />
                </UFormField>
                <div class="col-span-2 flex justify-end items-center mt-6 gap-4">
                    <UButton @click="currentForm = 0" color="neutral" label="Précédant" />
                    <UButton type="submit" :loading="createLoading" label="Créer" color="success" />
                </div>
            </UForm>
        </template>
    </UModal>
</template>