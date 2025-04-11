<template>
  <div class="space-y-6">
    <!-- Sélection médecin -->
    <div>
      <USelect
        v-model="formData.medecin_id"
        :options="formattedMedecins"
        label="Médecin"
        placeholder="Sélectionner un médecin"
        required
      />
    </div>

    <!-- Type de consultation -->
    <div>
      <USelect
        v-model="formData.type_consultation"
        :options="[
          { label: 'Première visite', value: 'premiere_visite' },
          { label: 'Suivi', value: 'suivi' },
          { label: 'Urgence', value: 'urgence' }
        ]"
        label="Type de consultation"
        required
      />
    </div>

    <!-- Date et heure -->
    <div>
      <UInput
        v-model="formData.date"
        type="datetime-local"
        label="Date et heure"
        required
      />
    </div>

    <!-- Motif -->
    <div>
      <UTextarea
        v-model="formData.motif"
        label="Motif de consultation"
        placeholder="Décrivez le motif de la consultation..."
        rows="3"
        required
      />
    </div>

    <!-- Symptômes -->
    <div>
      <UTextarea
        v-model="formData.symptomes"
        label="Symptômes"
        placeholder="Décrivez les symptômes..."
        rows="3"
        required
      />
    </div>

    <!-- Diagnostic -->
    <div>
      <UTextarea
        v-model="formData.diagnostic"
        label="Diagnostic"
        placeholder="Entrez le diagnostic..."
        rows="3"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  medecins: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'validate'])

const formData = ref({
  medecin_id: '',
  type_consultation: '',
  date: '',
  motif: '',
  symptomes: '',
  diagnostic: ''
})

const formattedMedecins = computed(() => {
  return props.medecins.map(medecin => ({
    label: `Dr. ${medecin.first_name} ${medecin.last_name}`,
    value: medecin.id
  }))
})

const isValid = computed(() => {
  return formData.value.medecin_id &&
         formData.value.type_consultation &&
         formData.value.date &&
         formData.value.motif &&
         formData.value.symptomes
})

watch(formData, (newValue) => {
  emit('update:modelValue', { ...newValue })
  emit('validate', isValid.value)
}, { deep: true })
</script>