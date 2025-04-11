<script lang="ts" setup>
import type { Patient } from '~/types';
import type { FormError, FormSubmitEvent } from '@nuxt/ui'

const props = defineProps({
    patient: {
        type: Object as PropType<Patient>,
        required: false,
    },
})

const model = defineModel({
    type: Boolean
})
const emit = defineEmits(['create', 'update'])
const toast = useToast()
const loading = ref(false)

const sexeOptions = [
    { label: 'Masculin', value: 'M' },
    { label: 'Féminin', value: 'F' },
    { label: 'Autre', value: 'A' },
]

const stadeOptions = [
    { label: 'Pas malade', value: 0 },
    { label: 'Stade 1', value: 1 },
    { label: 'Stade 2', value: 2 },
    { label: 'Stade 3', value: 3 },
    { label: 'Stade 4', value: 4 },
    { label: 'Stade 5', value: 5 },
]

const state = reactive({
    numero_dossier: "",
    nom: "",
    prenom: "",
    date_naissance: "",
    sexe: "M",
    telephone: "",
    email: "",
    adresse: "",
    stade_mrc: 0,
    dfu: "" as number | string,
    antecedents_medicaux: "",
    allergies: "",
})

watch(() => model.value, () => {
    if (props.patient) {
        state.numero_dossier = props.patient.numero_dossier
        state.nom = props.patient.nom
        state.prenom = props.patient.prenom
        state.date_naissance = props.patient.date_naissance
        state.sexe = props.patient.sexe
        state.telephone = props.patient.telephone
        state.email = props.patient.email || ""
        state.adresse = props.patient.adresse
        state.stade_mrc = props.patient.stade_mrc || 0
        state.dfu = props.patient.dfu || ""
        state.antecedents_medicaux = props.patient.antecedents_medicaux || ""
        state.allergies = props.patient.allergies || ""
    } else {
        resetForm()
    }
})

const validate = (state: any): FormError[] => {
    const errors = []
    if (!state.nom) errors.push({ name: 'nom', message: 'Veuillez entrer le nom' })
    if (!state.prenom) errors.push({ name: 'prenom', message: 'Veuillez entrer le prénom' })
    if (state.email) {
        if (!/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/.test(state.email))
            errors.push({ name: 'email', message: 'Veuillez entrer un email valide' })
    }
    if (!state.date_naissance) errors.push({ name: 'date_naissance', message: 'Veuillez entrer la date de naissance' })
    else if (!/^\d{4}-\d{2}-\d{2}$/.test(state.date_naissance)) {
        errors.push({ name: 'date_naissance', message: 'Veuillez entrer une date valide' })
    }
    else if (new Date(state.date_naissance) > new Date()) {
        errors.push({ name: 'date_naissance', message: 'La date de naissance ne peut pas être dans le futur' })
    }
    if (!state.telephone) errors.push({ name: 'telephone', message: 'Veuillez entrer le numéro' })
    if (!state.adresse) errors.push({ name: 'adresse', message: 'Veuillez entrer l\'adresse' })
    return errors
}

function resetForm() {
    state.numero_dossier = ""
    state.nom = ""
    state.prenom = ""
    state.date_naissance = ""
    state.sexe = "M"
    state.telephone = ""
    state.email = ""
    state.adresse = ""
    state.stade_mrc = 0
    state.dfu = ""
    state.antecedents_medicaux = ""
    state.allergies = ""
}

async function onSubmit(event: FormSubmitEvent<any>) {
    loading.value = true
    const body = event.data
    body['stade_mrc'] = body.stade_mrc === 0 ? null : body.stade_mrc
    body['dfu'] = body.dfu === "" ? null : body.dfu
    body['antecedents_medicaux'] = body.antecedents_medicaux === "" ? null : body.antecedents_medicaux
    body['allergies'] = body.allergies === "" ? null : body.allergies
    body['email'] = body.email === "" ? null : body.email
    if (!state.numero_dossier) delete body.numero_dossier
    console.log('body', body)
    const res = await apiRequest<Patient>(
        () => $fetch(`/api/patients/${props.patient ? `${props.patient.id}/` : ''}`, {
            method: props.patient ? "PATCH" : "POST",
            body: body,
            credentials: "include"
        }),
        toast
    );
    if (res) {
        emit(props.patient ? 'update' : 'create', res)
        toast.add({
            title: `${res.nom} ${res.prenom}`,
            description: `Patient ${props.patient ? 'modifié' : 'créé'} avec succès`,
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
    <UModal v-model:open="model" :title="`${patient ? 'Modifier' : 'Ajouter'} un patient`"
        :description="`${patient ? 'Mettez à jour' : 'Remplissez'} les informations du patient`"
        :ui="{ content: 'max-w-4xl' }">
        <template #body>
            <UForm :state="state" :validate="validate" @submit="onSubmit">
                <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-12 gap-6">
                    <!-- Ligne 1 : Nom / Prénom / Date naissance -->
                    <UFormField class="xl:col-span-4" label="Nom" name="nom" required>
                        <UInput v-model="state.nom" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-4" label="Prénom(s)" name="prenom" required>
                        <UInput v-model="state.prenom" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-4" label="Date de naissance" name="date_naissance" required>
                        <UInput v-model="state.date_naissance" type="date" class="w-full" />
                    </UFormField>

                    <!-- Ligne 2 : Numéro dossier / Stade MRC / DFU -->
                    <UFormField class="xl:col-span-4" label="Numéro de dossier" name="numero_dossier">
                        <UInput v-model="state.numero_dossier" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-4" label="Stade MRC" name="stade_mrc">
                        <USelectMenu v-model="state.stade_mrc" value-key="value" label-key="label" :items="stadeOptions"
                            :search-input="false" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-4" label="DFU" name="dfu">
                        <UInput v-model="state.dfu" type="number" class="w-full">
                            <template #trailing>
                                <UBadge label=" mL / min / 1,73m²" color="neutral" variant="soft" />
                            </template>
                        </UInput>
                    </UFormField>

                    <!-- Ligne 3 : Sexe / Téléphone / Email -->
                    <UFormField class="xl:col-span-2" label="Sexe" name="sexe" required>
                        <USelectMenu v-model="state.sexe" value-key="value" label-key="label" :items="sexeOptions"
                            :search-input="false" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-4" label="Numéro de téléphone" name="telephone" required>
                        <UInput v-model="state.telephone" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-6" label="Email" name="email">
                        <UInput v-model="state.email" type="email" class="w-full" />
                    </UFormField>

                    <!-- Ligne 4 : Adresse (pleine largeur) -->
                    <UFormField class="xl:col-span-12" label="Adresse" name="adresse" required>
                        <UInput v-model="state.adresse" class="w-full" />
                    </UFormField>

                    <!-- Ligne 5 : Antécédents / Allergies (moitié chacun) -->
                    <UFormField class="xl:col-span-6" label="Antécédents médicaux" name="antecedents_medicaux">
                        <UTextarea v-model="state.antecedents_medicaux" :rows="5" class="w-full" />
                    </UFormField>

                    <UFormField class="xl:col-span-6" label="Allergies" name="allergies">
                        <UTextarea v-model="state.allergies" :rows="5" class="w-full" />
                    </UFormField>
                </div>
                <div class="mt-8 flex justify-center items-center gap-8">
                    <UButton label="Annuler" color="neutral" @click="model = false" />
                    <UButton :label="patient ? 'Modifier' : 'Enregistrer'" :loading="loading" type="submit"
                        :color="patient ? 'primary' : 'success'" />
                </div>
            </UForm>
        </template>
    </UModal>
</template>