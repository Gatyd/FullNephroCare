<template>
  <div v-if="modelValue" class="fixed inset-0 bg-black/75 dark:bg-black/90 backdrop-blur-sm flex items-center justify-center z-50">
    <UCard class="w-full max-w-2xl">
      <template #header>
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold text-blue-600 dark:text-blue-400">
            Détails de la consultation
          </h3>
          <UButton
            color="gray"
            variant="ghost"
            icon="i-heroicons-x-mark"
            @click="closeModal"
          />
        </div>
      </template>

      <div class="space-y-6" v-if="consultation">
        <!-- Patient Info -->
        <div class="border-b pb-4 dark:border-gray-700">
          <h4 class="font-medium mb-2 text-gray-700 dark:text-gray-300">Patient</h4>
          <div v-if="consultation.patient" class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Patient</p>
              <p class="text-gray-900 dark:text-gray-100">
                {{ consultation.patient.nom }} {{ consultation.patient.prenom }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">N° Dossier</p>
              <p class="text-gray-900 dark:text-gray-100">
                {{ consultation.patient.numero_dossier }}
              </p>
            </div>
          </div>
        </div>

        <!-- Médecin Info -->
        <div class="border-b pb-4 dark:border-gray-700">
          <h4 class="font-medium mb-2 text-gray-700 dark:text-gray-300">Médecin</h4>
          <div v-if="consultation.medecin" class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Médecin</p>
              <p class="text-gray-900 dark:text-gray-100">
                Dr. {{ consultation.medecin.first_name }} {{ consultation.medecin.last_name }}
              </p>
            </div>
          </div>
        </div>

        <!-- Consultation Details -->
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Date</p>
              <p class="text-gray-900 dark:text-gray-100">
                {{ formatDate(consultation.date) }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Type</p>
              <UBadge
                :color="getConsultationTypeColor(consultation.type_consultation)"
                variant="subtle"
                size="sm"
              >
                {{ consultation.type_consultation }}
              </UBadge>
            </div>
          </div>

          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Motif</p>
            <p class="text-gray-900 dark:text-gray-100">{{ consultation.motif }}</p>
          </div>

          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Symptômes</p>
            <p class="text-gray-900 dark:text-gray-100 whitespace-pre-line">{{ consultation.symptomes }}</p>
          </div>

          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Diagnostic</p>
            <p class="text-gray-900 dark:text-gray-100 whitespace-pre-line">{{ consultation.diagnostic }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <UButton
            color="gray"
            @click="closeModal"
          >
            Fermer
          </UButton>
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  consultation: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const closeModal = () => {
  emit('update:modelValue', false)
}

const formatDate = (dateString) => {
  if (!dateString) return 'Date non disponible'
  return new Date(dateString).toLocaleString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getConsultationTypeColor = (type) => {
  switch (type) {
    case 'Première visite': return 'blue'
    case 'Suivi': return 'green'
    case 'Urgence': return 'red'
    case 'Téléconsultation': return 'purple'
    default: return 'gray'
  }
}
</script>