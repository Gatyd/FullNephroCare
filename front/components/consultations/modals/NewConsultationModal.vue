<template>
  <div class="fixed inset-0 bg-black/75 dark:bg-black/90 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl mx-auto p-6">
      <!-- En-tête -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold text-blue-600 dark:text-blue-400">
          Nouvelle consultation - 
          {{ getStepTitle() }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100">
          &times;
        </button>
      </div>

      <!-- Barre de progression -->
      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mb-6">
        <div class="h-2.5 rounded-full bg-blue-500 dark:bg-blue-600" 
             :style="{ width: `${(currentStep / 5) * 100}%` }">
        </div>
      </div>

      <!-- Contenu dynamique -->
      <div class="overflow-y-auto max-h-[calc(80vh-180px)]">
        <component 
          :is="currentStepComponent"
          v-model:consultation-data="consultationData"
          v-model:patient-data="patientData"
          :patients="patients"
          :medecins="medecins"
          :errors="errors"
        />
        <PatientStep
          v-model="patientType"
          v-model:selectedPatient="selectedPatientId"
          v-model:newPatientData="newPatientData"
          :patients="patients"
          :errors="errors"
        />
      </div>

      <!-- Boutons de navigation -->
      <div class="flex justify-end mt-6 space-x-3">
        <button 
          v-if="currentStep > 1" 
          @click="previousStep"
          class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100 bg-gray-100 dark:bg-gray-700"
        >
          Précédent
        </button>
        
        <button 
          @click="$emit('close')"
          class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100 bg-gray-100 dark:bg-gray-700"
        >
          Annuler
        </button>
        
        <button 
          v-if="currentStep < 5"
          @click="nextStep"
          class="px-4 py-2 rounded-md text-white bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700"
        >
          Suivant
        </button>
        
        <button 
          v-else
          @click="saveConsultation"
          class="px-4 py-2 rounded-md text-white bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700"
        >
          Terminer
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import PatientStep from '../steps/PatientStep.vue'
import ConsultationDetailsStep from '../steps/ConsultationDetailsStep.vue'
import PrescriptionsStep from '../steps/PrescriptionsStep.vue'
import ExamenStep from '../steps/ExamenStep.vue'
import AppointmentStep from '../steps/AppointmentStep.vue'

export default {
  name: 'NewConsultationModal',

  components: {
    PatientStep,
    ConsultationDetailsStep,
    PrescriptionsStep,
    ExamenStep,
    AppointmentStep
  },

  props: {
    patients: {
      type: Array,
      required: true
    },
    medecins: {
      type: Array,
      required: true
    }
  },

  emits: ['close', 'save'],

  setup() {
    const currentStep = ref(1)
    const errors = reactive({})
    
    const consultationData = reactive({
      patient: null,
      medecin: null,
      date: new Date().toISOString().slice(0, 16),
      type_consultation: 'Première visite',
      motif: '',
      symptomes: '',
      diagnostic: '',
      prescriptions: []
    })

    const patientData = reactive({
      type: 'existing',
      selectedId: null,
      newPatient: {
        nom: '',
        prenom: '',
        date_naissance: '',
        sexe: 'M',
        // ... autres champs patient
      }
    })

    const patientType = ref('existing')
    const selectedPatientId = ref('')
    const newPatientData = reactive({
      nom: '',
      prenom: '',
      date_naissance: '',
      sexe: 'M'
    })

    // Méthodes
    const getStepTitle = () => {
      switch (currentStep.value) {
        case 1: return 'Patient'
        case 2: return 'Détails consultation'
        case 3: return 'Prescriptions'
        case 4: return 'Planification d\'examen'
        case 5: return 'Planification de rendez-vous'
        default: return ''
      }
    }

    // Autre logique de composant...

    return {
      currentStep,
      errors,
      consultationData,
      patientData,
      getStepTitle,
      patientType,
      selectedPatientId,
      newPatientData,
      // ... autres méthodes et propriétés
    }
  }
}
</script>