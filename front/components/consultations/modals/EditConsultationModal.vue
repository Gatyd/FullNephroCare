<template>
  <div class="fixed inset-0 bg-black/75 dark:bg-black/90 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl mx-auto p-6">
      <ModalHeader 
        title="Modifier la consultation" 
        @close="$emit('close')" 
      />

      <div class="overflow-y-auto max-h-[calc(80vh-180px)]">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Informations de base -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Médecin -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Médecin
              </label>
              <select 
                v-model="formData.medecin_id"
                class="w-full px-4 py-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
              >
                <option v-for="medecin in medecins" 
                        :key="medecin.id" 
                        :value="medecin.id">
                  Dr. {{ medecin.first_name }} {{ medecin.last_name }}
                </option>
              </select>
            </div>

            <!-- Date -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Date
              </label>
              <input 
                v-model="formData.date"
                type="datetime-local"
                class="w-full px-4 py-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
              >
            </div>

            <!-- Type de consultation -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Type de consultation
              </label>
              <select 
                v-model="formData.type_consultation"
                class="w-full px-4 py-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
              >
                <option value="Première visite">Première visite</option>
                <option value="Suivi">Suivi</option>
                <option value="Urgence">Urgence</option>
              </select>
            </div>

            <!-- Motif -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Motif
              </label>
              <input 
                v-model="formData.motif"
                type="text"
                class="w-full px-4 py-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
              >
            </div>

            <!-- Symptômes -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Symptômes
              </label>
              <textarea 
                v-model="formData.symptomes"
                rows="3"
                class="w-full px-4 py-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
              ></textarea>
            </div>

            <!-- Diagnostic -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Diagnostic
              </label>
              <textarea 
                v-model="formData.diagnostic"
                rows="3"
                class="w-full px-4 py-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
              ></textarea>
            </div>
          </div>
        </form>
      </div>

      <ModalFooter
        @cancel="$emit('close')"
        @save="handleSubmit"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ModalHeader from '../shared/ModalHeader.vue'
import ModalFooter from '../shared/ModalFooter.vue'

export default {
  name: 'EditConsultationModal',

  components: {
    ModalHeader,
    ModalFooter
  },

  props: {
    consultation: {
      type: Object,
      required: true
    },
    medecins: {
      type: Array,
      required: true
    }
  },

  emits: ['close', 'save'],

  setup(props) {
    const formData = ref({
      medecin_id: '',
      date: '',
      type_consultation: '',
      motif: '',
      symptomes: '',
      diagnostic: ''
    })

    onMounted(() => {
      // Pré-remplir le formulaire avec les données existantes
      formData.value = {
        medecin_id: props.consultation.medecin_id,
        date: props.consultation.date,
        type_consultation: props.consultation.type_consultation,
        motif: props.consultation.motif,
        symptomes: props.consultation.symptomes,
        diagnostic: props.consultation.diagnostic
      }
    })

    const handleSubmit = () => {
      emit('save', {
        ...formData.value,
        id: props.consultation.id
      })
    }

    return {
      formData,
      handleSubmit
    }
  }
}
</script>