<template>
  <div class="h-full w-full flex items-center justify-center">
    <h1>Consultations</h1>
  </div>
</template>
<!-- <template>
  <div class="min-h-screen bg-blue-50 dark:bg-gray-900 transition-colors duration-300">
    <div class="container mx-auto">
      <h1 class="text-xl font-bold text-blue-600 dark:text-white">
        Système de Gestion des Consultations
      </h1>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Composant de recherche 
      <SearchForm 
        v-model:search-patient="searchPatient"
        v-model:selected-medecin="selectedMedecinId"
        v-model:date-debut="dateDebut"
        v-model:date-fin="dateFin"
        :medecins="medecins"
        @reset="resetSearch"
        @new-consultation="openNewConsultationModal"
      />

      <!-- Table des consultations 
      <ConsultationsTable 
        :consultations="filteredConsultations"
        :current-page="currentPage"
        :per-page="perPage"
        :total="total"
        @view="viewConsultation"
        @edit="editConsultation"
        @delete="deleteConsultation"
        @page-change="handlePageChange"
      />

      <Pagination
        v-model:currentPage="currentPage"
        :per-page="perPage"
        :total="total"
      />
    </div>

    <!-- Modals 
    <NewConsultationModal
      v-if="showNewConsultationModal"
      :patients="patients"
      :medecins="medecins"
      @close="closeNewConsultationModal"
      @save="saveConsultation"
    />

    <ViewConsultationModal
      v-if="showViewModal"
      :consultation="selectedConsultation"
      @close="closeViewModal"
    />

    <EditConsultationModal
      v-if="showEditModal"
      :consultation="editingConsultation"
      :medecins="medecins"
      @close="closeEditModal"
      @save="saveEditedConsultation"
    />

    <!-- Toast pour les notifications 
    <Toast 
      v-model:show="showToast"
      :type="toastType"
      :title="toastTitle"
      :message="toastMessage"
    />

    <!-- Dialog de confirmation 
    <ConfirmationDialog
      v-if="showConfirmDialog"
      :title="confirmDialogTitle"
      :message="confirmDialogMessage"
      :type="confirmDialogType"
      @confirm="handleConfirmDialog"
      @cancel="closeConfirmDialog"
    />
  </div>
</template>

<script>
import { ref, computed } from 'vue'

// Forms
import SearchForm from '@/components/consultations/forms/SearchForm.vue'

// Tables
import ConsultationsTable from '@/components/consultations/tables/ConsultationsTable.vue'

// Modals
import NewConsultationModal from '@/components/consultations/modals/NewConsultationModal.vue'
import ViewConsultationModal from '@/components/consultations/modals/ViewConsultationModal.vue'
import EditConsultationModal from '@/components/consultations/modals/EditConsultationModal.vue'

// Steps
import PatientStep from '@/components/consultations/steps/PatientStep.vue'
import ConsultationDetailsStep from '@/components/consultations/steps/ConsultationDetailsStep.vue'
import PrescriptionsStep from '@/components/consultations/steps/PrescriptionsStep.vue'
import ExamenStep from '@/components/consultations/steps/ExamenStep.vue'
import AppointmentStep from '@/components/consultations/steps/AppointmentStep.vue'

// Shared Components
import Toast from '@/components/consultations/shared/Toast.vue'
import ConfirmationDialog from '@/components/consultations/shared/ConfirmationDialog.vue'
import Pagination from '@/components/consultations/shared/Pagination.vue'
import ModalHeader from '@/components/consultations/shared/ModalHeader.vue'
import ModalFooter from '@/components/consultations/shared/ModalFooter.vue'
import ProgressBar from '@/components/consultations/shared/ProgressBar.vue'
import DeleteConfirmationModal from '~/components/consultations/modals/DeleteConfirmationModal.vue'
import ConsultationStepsModal from '~/components/consultations/modals/ConsultationStepsModal.vue'

export default {
  components: {
    // Forms
    SearchForm,
    
    // Tables
    ConsultationsTable,
    
    // Modals
    NewConsultationModal,
    ViewConsultationModal,
    EditConsultationModal,
    DeleteConfirmationModal,
    ConsultationStepsModal,
    
    // Steps
    PatientStep,
    ConsultationDetailsStep,
    PrescriptionsStep,
    ExamenStep,
    AppointmentStep,
    
    // Shared Components
    Toast,
    ConfirmationDialog,
    Pagination,
    ModalHeader,
    ModalFooter,
    ProgressBar
  },

  setup() {
    // État
    const searchPatient = ref('')
    const selectedMedecinId = ref('')
    const dateDebut = ref('')
    const dateFin = ref('')
    const showNewConsultationModal = ref(false)
    const showViewModal = ref(false)
    const showEditModal = ref(false)
    const selectedConsultation = ref(null)
    const editingConsultation = ref(null)

    // Données simulées
    const patients = ref([])
    const medecins = ref([])
    const consultations = ref([])

    // Pagination
    const currentPage = ref(1)
    const perPage = ref(10)
    const total = computed(() => filteredConsultations.value.length)

    // Toast
    const showToast = ref(false)
    const toastType = ref('success')
    const toastTitle = ref('')
    const toastMessage = ref('')

    // Dialog de confirmation
    const showConfirmDialog = ref(false)
    const confirmDialogTitle = ref('')
    const confirmDialogMessage = ref('')
    const confirmDialogType = ref('primary')
    const confirmDialogCallback = ref(null)

    // Computed
    const filteredConsultations = computed(() => {
      let filtered = consultations.value

      if (searchPatient.value) {
        const searchTerm = searchPatient.value.toLowerCase()
        filtered = filtered.filter(consultation => {
          const patientFullName = `${consultation.patient.nom} ${consultation.patient.prenom}`.toLowerCase()
          return patientFullName.includes(searchTerm)
        })
      }

      // ... autres filtres

      return filtered
    })

    // Méthodes
    const loadData = async () => {
      // Charger les données depuis l'API
    }

    const showNotification = (type, title, message) => {
      toastType.value = type
      toastTitle.value = title
      toastMessage.value = message
      showToast.value = true
    }

    const openNewConsultationModal = () => {
      console.log('Opening modal')
      showNewConsultationModal.value = true
    }

    const closeNewConsultationModal = () => {
      showNewConsultationModal.value = false
    }

    const saveConsultation = (consultationData) => {
      // Logique pour sauvegarder la consultation
      console.log('Saving consultation:', consultationData)
      showNewConsultationModal.value = false
    }

    // ... autres méthodes nécessaires

    return {
      // État
      searchPatient,
      selectedMedecinId,
      dateDebut,
      dateFin,
      showNewConsultationModal,
      showViewModal,
      showEditModal,
      selectedConsultation,
      editingConsultation,
      
      // Données
      patients,
      medecins,
      consultations,
      
      // Computed
      filteredConsultations,
      
      // Méthodes
      loadData,
      showNotification,
      openNewConsultationModal,
      closeNewConsultationModal,
      saveConsultation,
      // ... autres propriétés et méthodes
    }
  }
}
</script> -->