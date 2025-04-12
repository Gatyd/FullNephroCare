<script lang="ts" setup>
import type { Consultation, Examen } from '~/types';
import type { FormError, FormSubmitEvent } from '@nuxt/ui';

const props = defineProps({
    examen: {
        type: Object as PropType<Examen>,
        required: false,
    },
    essai:{
        type: String,
        required:false,
    }

});

const model = defineModel({
    type: Boolean
});

const emit = defineEmits(['create', 'update']);
const toast = useToast();
const loading = ref(false);
const patientId = ref(0);

const state = reactive({
    patient: 0,
    type_examen: "",
    description: "",
    date_realisation: "", // Date
    urgence: false,
    resultat: 0,
    date_creation: "", 
});

const validate = (state: any): FormError[] => {
    const errors = []
    if (!state.type_examen) errors.push({ name: 'type_examen', message: 'Veuillez entrer le type d\'examen ' })
    if (!state.patient) errors.push({ name: 'patient', message: 'Veuillez sélectionner le patient ' })
    if (!state.date_realisation) errors.push({ name: 'date_realisation', message: 'Veuillez entrer la date de realisation' })
    else if (new Date(state.date_realisation) < new Date()) {
        errors.push({ name: 'date_realisation', message: 'La date de réalisation ne peut pas être dans le passé' })
    }
    return errors
}
function resetForm() {
    state.patient = 0;
    state.type_examen = "";
    state.description = "";
    state.date_realisation = "";
    state.urgence = false;
    state.resultat = 0;
    state.date_creation = "";
}

async function onSubmit(event: FormSubmitEvent<any>){
    loading.value = true
    const body = event.data
    console.log(body)
    body['description'] = body.description === "" ? null : body.description
    body['resultat'] = body.resultat === 0 ? null : body.resultat
    body['patient'] = body.patient === 0 ? null : body.patient
    body['urgence'] = body.urgence === false ? 0: 1
    if(props.examen)
    {
        console.log(props.examen.id)
    }
    const res = await apiRequest<Examen>(
        () => $fetch(`/api/examens/${props.examen ? `${props.examen.id}/` : ''}`, {
            method: props.examen ? "PATCH" : "POST",
            body: body,
            credentials: "include"
        }),
        toast
    );
    if (res) {
        emit(props.examen ? 'update' : 'create', res)
        toast.add({
            title: `${res.type_examen}`,
            description: `Examen ${props.examen ? 'modifié' : 'créé'} avec succès`,
            color: "success",
            icon: "i-heroicons-check-circle",
            duration: 3000,
        })
        resetForm()
        model.value = false
    }
    loading.value = false
}

watch(() => model.value, async () => {
  const examen = props.examen;

  if (examen) {
    state.patient = (examen.consultation as Consultation).patient.id;
    state.type_examen = examen.type_examen;
    state.description = examen.description ?? "";
    state.date_realisation = examen.date_realisation;
    state.urgence = examen.urgence;
    state.resultat = examen.resultat ?? 0;

  } else {
    resetForm();
  }
}); 



</script>

<template>
    <UModal
        v-model:open="model"
        :title="props.examen ? 'Modifier un examen' : 'Ajouter un examen'"
        :description="props.examen ? 'Modifiez les informations de l\'examen' : 'Remplissez les informations de l\'examen'"
    >
        <template #body>
            <UForm :state="state" :validate="validate" @submit="onSubmit">
                <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-12 gap-6">
                    <PatientSelectMenu v-model="state.patient" class="xl:col-span-6"/>
                    <UFormField class="xl:col-span-6" label="Type d'examen" name="type_examen" required>
                        <UInput v-model="state.type_examen" class="w-full " />
                    </UFormField>

                    <UFormField class="xl:col-span-12 my-1" label="description" name="description">
                        <UTextarea v-model="state.description" :rows="5" class="w-full" />
                    </UFormField>
                    <UFormField class="xl:col-span-12 my-1" label="Date de réalisation" name="date_realisation" required>
                        <UInput v-model="state.date_realisation" type="datetime-local" class="w-full" />
                    </UFormField>
                    <UFormField class="xl:col-span-12 my-1" name="urgence" required >
                        <UCheckbox v-model="state.urgence" class="w-full " label="Urgent" />
                    </UFormField>
                </div>
                <div class="mt-8 flex justify-center items-center gap-8">
                    <UButton label="Annuler" color="neutral" @click="model = false" />
                    <UButton label="Enregistrer" :loading="loading" type="submit" color="success"/>
                </div>
            </UForm>
        </template>
    </UModal>
</template>

