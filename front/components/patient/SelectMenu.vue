<script setup lang="ts">
import type { Patient } from '~/types';

const model = defineModel({
    type: Number
})

const loading = ref(true)
const patients = ref<Array<any> | undefined>([])
const toast = useToast()

async function fetchPatients(){
    loading.value = true
    patients.value = await apiRequest<Array<any>>(
        () => $fetch('/api/patients/', {
            method: 'GET',
            key: 'patients',
            credentials: "include"
        }),
        toast
    ) as Array<Patient> | undefined
    patients.value?.map((patient) => {
        patient.label = `${patient.nom} ${patient.prenom}`
        return patient
    })
    loading.value = false
}

onMounted(() => {
    fetchPatients()
})
</script>
<template>
    <UFormField  v-bind="$attrs" label="Patient" name="patient" :required="true">
        <USelect v-model="model" placeholder="Sélectionner un patient" :loading="loading" :clearable="true"
        :items="patients" value-key="id" label-key="label" class="w-full  xl:col-span-6" />
    </UFormField>
</template>