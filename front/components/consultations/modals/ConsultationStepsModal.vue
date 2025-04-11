<template>
  <div v-if="modelValue" class="fixed inset-0 bg-black/75 dark:bg-black/90 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl mx-auto p-6">
      <!-- En-tête -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold text-blue-600 dark:text-blue-400">
          Nouvelle consultation - 
          {{ currentStep === 1 ? 'Patient' : 
             currentStep === 2 ? 'Détails consultation' : 
             currentStep === 3 ? 'Prescriptions' :
             currentStep === 4 ? 'Planification d\'examen' :
             'Planification de rendez-vous' }}
        </h2>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100">
          &times;
        </button>
      </div>

      <!-- Barre de progression -->
      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mb-6">
        <div class="h-2.5 rounded-full bg-blue-500 dark:bg-blue-600" 
             :style="{ width: `${(currentStep / 5) * 100}%` }">
        </div>
      </div>

      <!-- Contenu avec scrollbar -->
      <div class="overflow-y-auto max-h-[calc(80vh-180px)]" :class="{ 'overflow-visible': currentStep === 2 }">
        <keep-alive>
          <component 
            :is="currentStepComponent"
            :patients="patients"
            :medecins="medecins"
            :patient-type="formData.patientType"
            :selected-patient-id="formData.selectedPatientId"
            :consultation-data="formData.consultation"
            :prescriptions="formData.prescriptions"
            :examen-data="formData.examen"
            :appointment-data="formData.appointment"
            :theme="theme"
            :errors="errors"
            @update:patient-type="updatePatientType"
            @update:selected-patient="updateSelectedPatient"
            @update:consultation="updateConsultation"
            @update:prescriptions="updatePrescriptions"
            @update:examen="updateExamen"
            @update:appointment="updateAppointment"
            @validate="validateStep"
          />
        </keep-alive>
      </div>

      <!-- Boutons footer -->
      <div class="flex justify-end mt-6 space-x-3">
        <button 
          v-if="currentStep > 1" 
          @click="previousStep" 
          class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100"
          :class="theme === 'dark' ? 'bg-gray-700 hover:bg-gray-800' : 'bg-gray-100 hover:bg-gray-200'"
        >
          Précédent
        </button>
        <button 
          @click="closeModal" 
          class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100"
          :class="theme === 'dark' ? 'bg-gray-700 hover:bg-gray-800' : 'bg-gray-100 hover:bg-gray-200'"
        >
          Annuler
        </button>
        <button 
          v-if="currentStep < 5"
          @click="nextStep" 
          class="px-4 py-2 rounded-md text-white font-medium transition-colors duration-200"
          :class="theme === 'dark' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'"
        >
          Suivant
        </button>
        <button 
          v-else
          @click="submitForm" 
          class="px-4 py-2 rounded-md text-white font-medium transition-colors duration-200"
          :class="theme === 'dark' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'"
        >
          Terminer
        </button>
      </div>
    </div>

    <!-- Modal de confirmation pour Annuler -->
    <div v-if="showCancelConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[60]">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium mb-4 text-gray-900 dark:text-gray-100">
          Confirmer l'annulation
        </h3>
        <p class="text-gray-600 dark:text-gray-300 mb-6">
          Êtes-vous sûr de vouloir annuler ? Toutes les informations non enregistrées seront perdues.
        </p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="cancelClose"
            class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600"
          >
            Non
          </button>
          <button 
            @click="confirmClose"
            class="px-4 py-2 rounded-md text-white bg-red-500 hover:bg-red-600"
          >
            Oui, annuler
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmation pour Terminer -->
    <div v-if="showSubmitConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[60]">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium mb-4 text-gray-900 dark:text-gray-100">
          Confirmer l'enregistrement
        </h3>
        <p class="text-gray-600 dark:text-gray-300 mb-6">
          Voulez-vous enregistrer cette consultation ?
        </p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="cancelSubmit"
            class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600"
          >
            Annuler
          </button>
          <button 
            @click="confirmSubmit"
            class="px-4 py-2 rounded-md text-white bg-green-500 hover:bg-green-600"
          >
            Oui, enregistrer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import PatientStep from '../steps/PatientStep.vue'
import ConsultationDetailsStep from '../steps/ConsultationDetailsStep.vue'
import PrescriptionsStep from '../steps/PrescriptionsStep.vue'
import ExamenStep from '../steps/ExamenStep.vue'
import AppointmentStep from '../steps/AppointmentStep.vue'

const props = defineProps({
  modelValue: Boolean,
  patients: {
    type: Array,
    required: true
  },
  medecins: {
    type: Array,
    required: true
  },
  theme: {
    type: String,
    default: 'light'
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

const currentStep = ref(1)
const errors = ref({})
const isStepValid = ref(true)

// Données du formulaire
const formData = ref({
  patientType: 'existing',
  selectedPatientId: null,
  consultation: {
    medecin: null,
    date: new Date().toISOString().slice(0, 16),
    type_consultation: 'Première visite',
    motif: '',
    symptomes: '',
    diagnostic: ''
  },
  prescriptions: [],
  examen: {
    type_examen: '',
    description: '',
    date_realisation: '',
    urgence: false
  },
  appointment: {
    date: '',
    time: '',
    type: 'suivi',
    notes: ''
  }
})

const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 1: return PatientStep
    case 2: return ConsultationDetailsStep
    case 3: return PrescriptionsStep
    case 4: return ExamenStep
    case 5: return AppointmentStep
    default: return PatientStep
  }
})

// Méthodes de mise à jour des données
const updatePatientType = (value) => {
  formData.value.patientType = value
}

const updateSelectedPatient = (value) => {
  formData.value.selectedPatientId = value
}

const updateConsultation = (value) => {
  formData.value.consultation = value
}

const updatePrescriptions = (value) => {
  formData.value.prescriptions = value
}

const updateExamen = (value) => {
  formData.value.examen = value
}

const updateAppointment = (value) => {
  formData.value.appointment = value
}

const validateStep = (isValid) => {
  isStepValid.value = isValid
}

const nextStep = () => {
  if (isStepValid.value && currentStep.value < 5) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const closeModal = () => {
  showCancelConfirm.value = true
}

const confirmClose = () => {
  showCancelConfirm.value = false
  emit('update:modelValue', false)
}

const cancelClose = () => {
  showCancelConfirm.value = false
}

const submitForm = () => {
  if (isStepValid.value) {
    showSubmitConfirm.value = true
  }
}

const confirmSubmit = () => {
  emit('save', formData.value)
  showSubmitConfirm.value = false
  emit('update:modelValue', false)
}

const cancelSubmit = () => {
  showSubmitConfirm.value = false
}

// Ajout des refs pour les confirmations
const showCancelConfirm = ref(false)
const showSubmitConfirm = ref(false)
</script>