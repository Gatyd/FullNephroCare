<template>
  <div>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Patient
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Médecin
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Date
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="consultation in paginatedConsultations" 
                :key="consultation.id"
                class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-150"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center" v-if="consultation && consultation.patient">
                  <div class="flex-shrink-0 h-10 w-10">
                    <UAvatar
                      :text="getInitials(consultation.patient.nom, consultation.patient.prenom)"
                      size="sm"
                      :class="consultation.patient.sexe === 'M' ? 'bg-blue-100 text-blue-600' : 'bg-pink-100 text-pink-600'"
                    />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-gray-100">
                      {{ consultation.patient.nom }} {{ consultation.patient.prenom }}
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      ID: {{ consultation.patient.id }}
                    </div>
                  </div>
                </div>
                <div v-else class="text-sm text-gray-500">
                  Données patient non disponibles
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div v-if="consultation && consultation.medecin">
                  <div class="text-sm text-gray-900 dark:text-gray-100">
                    Dr. {{ consultation.medecin.first_name }} {{ consultation.medecin.last_name }}
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">
                    Néphrologue
                  </div>
                </div>
                <div v-else class="text-sm text-gray-500">
                  Médecin non assigné
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-gray-100">
                  {{ formatDate(consultation.date) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <UBadge
                  :color="getConsultationTypeColor(consultation.type_consultation)"
                  variant="subtle"
                  size="sm"
                >
                  {{ consultation.type_consultation }}
                </UBadge>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                <div class="flex items-center space-x-3">
                  <UTooltip text="Voir les détails">
                    <UButton
                      color="blue"
                      variant="solid"
                      icon="i-heroicons-eye"
                      size="sm"
                      @click="openViewModal(consultation)"
                      class="text-white bg-blue-500 hover:bg-blue-500"
                    />
                  </UTooltip>
                  <UTooltip text="Modifier">
                    <UButton
                      color="blue"
                      variant="solid"
                      icon="i-heroicons-pencil-square"
                      size="sm"
                      @click="openEditModal(consultation)"
                      class="text-white bg-blue-500 hover:bg-blue-500"
                    />
                  </UTooltip>
                  <UTooltip text="Supprimer">
                    <UButton
                      color="red"
                      variant="solid"
                      icon="i-heroicons-trash"
                      size="sm"
                      @click="openDeleteModal(consultation)"
                      class="text-white bg-red-600 hover:bg-red-700"
                    />
                  </UTooltip>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <ViewConsultationModal
      v-model="showViewModal"
      :consultation="selectedConsultation"
    />

    <EditConsultationModal
      v-model="showEditModal"
      :consultation="selectedConsultation"
      :medecins="medecins"
      @update="handleUpdate"
      @save="saveConsultation"
      @close="closeModal"
    />

    <DeleteConfirmationModal
      v-model="showDeleteModal"
      :item-name="`la consultation du ${selectedConsultation ? formatDate(selectedConsultation.date) : ''}`"
      :theme="theme"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ViewConsultationModal from '../modals/ViewConsultationModal.vue'
import EditConsultationModal from '../modals/EditConsultationModal.vue'
import DeleteConfirmationModal from '../modals/DeleteConfirmationModal.vue'

// Props avec validation plus stricte
const props = defineProps({
  consultations: {
    type: Array,
    required: true,
    default: () => []
  },
  currentPage: {
    type: Number,
    default: 1,
    validator: (value) => value > 0
  },
  perPage: {
    type: Number,
    default: 10,
    validator: (value) => value > 0
  },
  theme: {
    type: String,
    default: 'light',
    validator: (value) => ['light', 'dark'].includes(value)
  }
})

const emit = defineEmits(['view', 'edit', 'delete'])

// Reactive references
const showViewModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const selectedConsultation = ref(null)

// Computed properties
const paginatedConsultations = computed(() => {
  const start = (props.currentPage - 1) * props.perPage
  const end = start + props.perPage
  return props.consultations.slice(start, end)
})

// Utility functions
const formatDate = (dateString) => {
  if (!dateString) return 'Date non disponible'
  
  try {
    return new Date(dateString).toLocaleString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    console.error('Error formatting date:', error)
    return 'Date invalide'
  }
}

const getInitials = (nom = '', prenom = '') => {
  return `${nom.charAt(0)}${prenom.charAt(0)}`.toUpperCase()
}

const getConsultationTypeColor = (type) => {
  const typeColors = {
    'Première visite': 'blue',
    'Suivi': 'green',
    'Urgence': 'red',
    'Téléconsultation': 'purple'
  }
  return typeColors[type] || 'gray'
}

// Modal handlers
const openViewModal = (consultation) => {
  selectedConsultation.value = structuredClone(consultation)
  showViewModal.value = true
}

const openEditModal = (consultation) => {
  selectedConsultation.value = structuredClone(consultation)
  showEditModal.value = true
}

const openDeleteModal = (consultation) => {
  selectedConsultation.value = structuredClone(consultation)
  showDeleteModal.value = true
}

// Action handlers
const handleUpdate = (updatedConsultation) => {
  try {
    emit('edit', updatedConsultation)
    showEditModal.value = false
    selectedConsultation.value = null
  } catch (error) {
    console.error('Error updating consultation:', error)
  }
}

const handleDelete = () => {
  try {
    if (selectedConsultation.value) {
      emit('delete', selectedConsultation.value.id)
      showDeleteModal.value = false
      selectedConsultation.value = null
    }
  } catch (error) {
    console.error('Error deleting consultation:', error)
  }
}

// Reset function
const resetModals = () => {
  showViewModal.value = false
  showEditModal.value = false
  showDeleteModal.value = false
  selectedConsultation.value = null
}

// Data
const medecins = ref([
  { id: 1, first_name: 'Jean', last_name: 'Dupont' },
  { id: 2, first_name: 'Marie', last_name: 'Martin' },
  { id: 3, first_name: 'Pierre', last_name: 'Bernard' },
  // ... autres médecins
])

// Methods
const saveConsultation = (consultationData) => {
  // Logique pour sauvegarder la consultation
  console.log('Consultation sauvegardée:', consultationData)
}

const closeModal = () => {
  // Logique pour fermer le modal
}
</script>