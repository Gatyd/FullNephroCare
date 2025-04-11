<template>
  <div class="space-y-6">
    <!-- Prochain rendez-vous -->
    <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <UInput
          v-model="appointment.date"
          type="date"
          label="Date"
          required
        />
        <UInput
          v-model="appointment.heure"
          type="time"
          label="Heure"
          required
        />
      </div>

      <div class="mt-4">
        <USelect
          v-model="appointment.type"
          :options="[
            { label: 'Suivi', value: 'suivi' },
            { label: 'Contrôle', value: 'controle' },
            { label: 'Résultats', value: 'resultats' }
          ]"
          label="Type de rendez-vous"
          required
        />
      </div>

      <div class="mt-4">
        <UTextarea
          v-model="appointment.notes"
          label="Notes"
          placeholder="Notes pour le prochain rendez-vous..."
          rows="3"
        />
      </div>

      <div class="mt-4">
        <p class="text-sm text-gray-500 dark:text-gray-400">
          * Les champs Date, Heure et Type sont obligatoires
        </p>
      </div>
    </div>

    <!-- Rappel -->
    <div class="flex items-center space-x-2">
      <UCheckbox
        v-model="appointment.rappel"
        label="Envoyer un rappel au patient"
      />
      <USelect
        v-if="appointment.rappel"
        v-model="appointment.delai_rappel"
        :options="[
          { label: '1 jour avant', value: '1' },
          { label: '2 jours avant', value: '2' },
          { label: '1 semaine avant', value: '7' }
        ]"
        class="w-40"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const emit = defineEmits(['update:modelValue', 'validate'])

const appointment = ref({
  date: '',
  heure: '',
  type: 'suivi',
  notes: '',
  rappel: false,
  delai_rappel: '1'
})

const isValid = computed(() => {
  return appointment.value.date && 
         appointment.value.heure && 
         appointment.value.type
})

watch(appointment, (newValue) => {
  emit('update:modelValue', newValue)
  emit('validate', isValid.value)
}, { deep: true })
</script>