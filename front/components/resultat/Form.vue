<script lang="ts" setup>
import type { ResultatExamen } from '~/types';
import type { FormError, FormSubmitEvent } from '@nuxt/ui';

const props = defineProps({
  resultat: {
    type: Object as PropType<ResultatExamen>,
    required: false,
  },
  essai: {
    type: String,
    required: false,
  }

});

const model = defineModel({
  type: Boolean
});

const emit = defineEmits(['create', 'update']);
const toast = useToast();
const loading = ref(false);

const state = reactive({
  patient: 0,
  examen_prescrit: 0,
  type_examen: "",
  date_realisation: "",
  laboratoire: "",
  resultats_texte: "",
  fichier: "",
  creatinine: 0,
  dfu: 0,
  proteinurie: 0,
  interpretation: "",
  est_anormal: false,
  date_ajout: "",
  ajoute_par: 0
});

const validate = (state: any): FormError[] => {
  const errors: FormError[] = [];

  if (!state.type_examen) {
    errors.push({ name: 'type_examen', message: 'Veuillez entrer le type d\'examen' });
  }

  if (!state.patient) {
    errors.push({ name: 'patient', message: 'Veuillez sélectionner le patient' });
  }

  if (!state.date_realisation) {
    errors.push({ name: 'date_realisation', message: 'Veuillez entrer la date de réalisation' });
  } else if (!/^\d{4}-\d{2}-\d{2}$/.test(state.date_realisation)) {
    errors.push({ name: 'date_realisation', message: 'Veuillez entrer une date valide (format AAAA-MM-JJ)' });
  }

  if (state.creatinine !== null && isNaN(state.creatinine)) {
    errors.push({ name: 'creatinine', message: 'Valeur de créatinine invalide' });
  }

  if (state.dfu !== null && isNaN(state.dfu)) {
    errors.push({ name: 'dfu', message: 'Valeur de DFU invalide' });
  }

  if (state.proteinurie !== null && isNaN(state.proteinurie)) {
    errors.push({ name: 'proteinurie', message: 'Valeur de protéinurie invalide' });
  }

  return errors;
}
function resetForm() {
  state.patient = 0;
  state.examen_prescrit = 0;
  state.type_examen = "";
  state.date_realisation = "";
  state.laboratoire = "";
  state.resultats_texte = "";
  state.fichier = "";
  state.creatinine = 0;
  state.dfu = 0;
  state.proteinurie = 0;
  state.interpretation = "";
  state.est_anormal = false;
  state.date_ajout = "";
  state.ajoute_par = 0;
}


async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true;
  const body = event.data;

  console.log(body);

  // Nettoyage / transformation des données avant envoi
  body['examen_prescrit'] = body.examen_prescrit || null;
  body['laboratoire'] = body.laboratoire || null;
  body['resultats_texte'] = body.resultats_texte || null;
  body['creatinine'] = body.creatinine === null || body.creatinine === '' ? null : body.creatinine;
  body['dfu'] = body.dfu === null || body.dfu === '' ? null : body.dfu;
  body['proteinurie'] = body.proteinurie === null || body.proteinurie === '' ? null : body.proteinurie;
  body['interpretation'] = body.interpretation || "";
  body['ajoute_par'] = body.ajoute_par || null;
  body['est_anormal'] = !!body.est_anormal;

  // Gestion de la requête POST ou PATCH
  const res = await apiRequest<ResultatExamen>(
    () => $fetch(`/api/resultats-examens/${props.resultat ? `${props.resultat.id}/` : ''}`, {
      method: props.resultat ? "PATCH" : "POST",
      body,
      credentials: "include"
    }),
    toast
  );

  // Succès
  if (res) {
    emit(props.resultat ? 'update' : 'create', res);
    toast.add({
      title: `Résultat d'examen`,
      description: `Résultat ${props.resultat ? 'modifié' : 'ajouté'} avec succès`,
      color: "success",
      icon: "i-heroicons-check-circle",
      duration: 3000,
    });
    resetForm();
    model.value = false;
  }

  loading.value = false;
}

watch(() => model.value, () => {
  if (props.resultat) {
    state.patient = props.resultat.patient;
    state.examen_prescrit = props.resultat.examen_prescrit ?? 0;
    state.type_examen = props.resultat.type_examen;
    state.date_realisation = props.resultat.date_realisation;
    state.laboratoire = props.resultat.laboratoire ?? "";
    state.resultats_texte = props.resultat.resultats_texte ?? "";
    state.creatinine = props.resultat.creatinine ?? 0;
    state.dfu = props.resultat.dfu ?? 0;
    state.proteinurie = props.resultat.proteinurie ?? 0;
    state.interpretation = props.resultat.interpretation ?? "";
    state.est_anormal = props.resultat.est_anormal;
    state.date_ajout = props.resultat.date_ajout;
    state.ajoute_par = props.resultat.ajoute_par ?? 0;
  } else {
    resetForm();
  }
});

</script>

<template>
  <UModal v-model:open="model" :ui="{ content: 'max-w-4xl' }"
    :title="props.resultat ? 'Modifier un résultat' : 'Ajouter un résultat'"
    :description="props.resultat ? 'Modifiez les informations du résultat' : 'Remplissez les informations du résultat'">
    <template #body>
      <UForm :state="state" :validate="validate" @submit="onSubmit">
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-12 gap-6">
          <PatientSelectMenu class="xl:col-span-4" v-model="state.patient" />

          <UFormField class="xl:col-span-4" label="Type d'examen" name="type_examen" required>
            <UInput v-model="state.type_examen" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-4" label="Date de réalisation" name="date_realisation" required>
            <UInput v-model="state.date_realisation" type="date" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-4" label="Laboratoire" name="laboratoire">
            <UInput v-model="state.laboratoire" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-4" label="Fichier des résultats" name="fichier_resultats">
            <UInput v-model="state.fichier" type="file" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-4 place-self-center" name="est_anormal">
            <UCheckbox v-model="state.est_anormal" label="Résultat anormal" />
          </UFormField>

          <UFormField class="xl:col-span-4" label="Créatinine" name="creatinine">
            <UInput v-model="state.creatinine" type="number" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-4" label="DFU" name="dfu">
            <UInput v-model="state.dfu" type="number" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-4" label="Protéinurie" name="proteinurie">
            <UInput v-model="state.proteinurie" type="number" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-6" label="Résultats (texte)" name="resultats_texte">
            <UTextarea v-model="state.resultats_texte" :rows="4" class="w-full" />
          </UFormField>

          <UFormField class="xl:col-span-6" label="Interpretation" name="interpretation">
            <UTextarea v-model="state.interpretation" :rows="4" class="w-full" />
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