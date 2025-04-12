<script lang="ts" setup>
import type { Prescription } from '~/types';
import type { FormError, FormSubmitEvent } from '@nuxt/ui';

const props = defineProps({
  prescription: {
    type: Object as PropType<Prescription>,
    required: false,
  },
});

const model = defineModel({ type: Boolean });

const emit = defineEmits(['create', 'update']);
const toast = useToast();
const loading = ref(false);

const state = reactive({
  patient: 0,
  medicament: '',
  posologie: '',
  duree_traitement: 0,
  instructions: '',
  est_convertie: false,
  date_conversion: '',
  date_creation: '',
});

const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.patient) errors.push({ name: 'patient', message: 'Veuillez sélectionner le patient ' })
  if (!state.medicament) errors.push({ name: 'medicament', message: 'Veuillez entrer le nom du médicament' });
  if (!state.posologie) errors.push({ name: 'posologie', message: 'Veuillez entrer la posologie' });
  if (!state.duree_traitement) errors.push({ name: 'duree_traitement', message: 'Veuillez entrer la durée du traitement' });
  return errors;
};

function resetForm() {
  state.patient = 0;
  state.medicament = '';
  state.posologie = '';
  state.duree_traitement = 0;
  state.instructions = '';
  state.est_convertie = false;
  state.date_conversion = '';
  state.date_creation = '';
}

async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true;
  const body = event.data;

  body.instructions = body.instructions === '' ? null : body.instructions;
  body.consultation = body.consultation === 0 ? null : body.consultation;
  body['patient'] = body.patient === 0 ? null : body.patient
  body.date_conversion = body.date_conversion === '' ? null : body.date_conversion;
  body.est_convertie = body.est_convertie ? 1 : 0;

  const res = await apiRequest<Prescription>(
    () => $fetch(`/api/prescriptions/${props.prescription ? `${props.prescription.id}/` : ''}`, {
      method: props.prescription ? 'PATCH' : 'POST',
      body,
      credentials: 'include',
    }),
    toast
  );

  if (res) {
    emit(props.prescription ? 'update' : 'create', res);
    toast.add({
      title: res.medicament,
      description: `Prescription ${props.prescription ? 'modifiée' : 'créée'} avec succès`,
      color: 'success',
      icon: 'i-heroicons-check-circle',
      duration: 3000,
    });
    resetForm();
    model.value = false;
  }

  loading.value = false;
}

watch(() => model.value, async() => {
  const presc = props.prescription;
  if (presc) {
    try {
      const { patient } = await $fetch(`/api/consultations/${presc.consultation}`, {
        credentials: 'include'
      });
      state.patient = patient;
    } catch (error) {
      console.error("Impossible de récupérer l'examen avec patient", error);
      state.patient = 0;
    }

    state.medicament = presc.medicament;
    state.posologie = presc.posologie;
    state.duree_traitement = presc.duree_traitement;
    state.instructions = presc.instructions ?? '';
    state.est_convertie = presc.est_convertie;
    state.date_conversion = presc.date_conversion ?? '';
    state.date_creation = presc.date_creation;

  } else {
    resetForm();
  }
});
</script>
<template>
    <UModal
      v-model:open="model"
      :title="props.prescription ? 'Modifier une prescription' : 'Ajouter une prescription'"
      :description="props.prescription ? 'Modifiez les informations de la prescription' : 'Remplissez les informations de la prescription'"
    >
      <template #body>
        <UForm :state="state" :validate="validate" @submit="onSubmit">
          <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-12 gap-6">
            <PatientSelectMenu class="xl:col-span-6" v-model="state.patient" />
  
            <UFormField class="xl:col-span-6" label="Médicament" name="medicament" required>
              <UInput v-model="state.medicament" class="w-full" />
            </UFormField>
  
            <UFormField class="xl:col-span-6" label="Posologie" name="posologie" required>
              <UInput v-model="state.posologie" class="w-full" />
            </UFormField>
            
            <UFormField class="xl:col-span-6" label="Durée du traitement (jours)" name="duree_traitement" required>
              <UInput v-model="state.duree_traitement" type="number" min="1" class="w-full" />
            </UFormField>
            
            <UFormField class="xl:col-span-12 my-1" label="Date de conversion" name="date_conversion">
              <UInput v-model="state.date_conversion" type="date" class="w-full" />
            </UFormField>
            <UFormField class="xl:col-span-12" label="Instructions supplémentaires" name="instructions">
              <UTextarea v-model="state.instructions" :rows="3" class="w-full" />
            </UFormField>
            
            <UFormField class="xl:col-span-12" name="est_convertie">
              <UCheckbox v-model="state.est_convertie" label="Prescription convertie" />
            </UFormField>
          </div>
          
          <div class="mt-8 flex justify-center items-center gap-8">
            <UButton label="Annuler" color="neutral" @click="model = false" />
            <UButton label="Enregistrer" :loading="loading" type="submit" color="success" />
          </div>
        </UForm>
      </template>
    </UModal>
</template>
  
