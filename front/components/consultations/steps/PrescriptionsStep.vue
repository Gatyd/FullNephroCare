<template>
  <div class="space-y-6">
    <!-- Liste des prescriptions -->
    <div class="space-y-4">
      <div v-for="(prescription, index) in prescriptions" :key="index" class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UInput
            v-model="prescription.medicament"
            label="Médicament"
            placeholder="Nom du médicament"
          />
          <UInput
            v-model="prescription.dosage"
            label="Dosage"
            placeholder="Ex: 1 comprimé 3x/jour"
          />
        </div>
        <div class="mt-4">
          <UTextarea
            v-model="prescription.instructions"
            label="Instructions"
            placeholder="Instructions particulières..."
            rows="2"
          />
        </div>
        <div class="mt-4 flex justify-end">
          <UButton
            color="red"
            variant="soft"
            @click="removePrescription(index)"
            icon="i-heroicons-trash"
          >
            Supprimer
          </UButton>
        </div>
      </div>
    </div>

    <!-- Bouton ajouter -->
    <div class="flex justify-center">
      <UButton
        color="blue"
        variant="soft"
        @click="addPrescription"
        icon="i-heroicons-plus"
      >
        Ajouter une prescription
      </UButton>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const emit = defineEmits(['update:modelValue', 'validate'])

const prescriptions = ref([])

const addPrescription = () => {
  prescriptions.value.push({
    medicament: '',
    dosage: '',
    instructions: ''
  })
}

const removePrescription = (index) => {
  prescriptions.value.splice(index, 1)
}

watch(prescriptions, (newValue) => {
  emit('update:modelValue', newValue)
  emit('validate', prescriptions.value.length > 0)
}, { deep: true })

// Ajouter une première prescription vide au démarrage
addPrescription()
</script>