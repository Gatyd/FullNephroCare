<template>
  <div class="mb-4">
    <h3 class="text-lg font-medium mb-4" 
        :class="theme === 'dark' ? 'text-blue-400' : 'text-blue-600'">
      Planification d'examen
    </h3>

    <div class="space-y-4">
      <!-- Type d'examen -->
      <div>
        <label class="block text-sm text-gray-500 dark:text-gray-400 mb-1">
          Type d'examen
        </label>
        <select v-model="examenData.type_examen"
                :class="selectClasses"
                @change="updateExamen('type_examen', $event.target.value)">
          <option v-for="type in typesExamen" 
                  :key="type.value" 
                  :value="type.value">
            {{ type.label }}
          </option>
        </select>
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm text-gray-500 dark:text-gray-400 mb-1">
          Description
        </label>
        <textarea v-model="examenData.description"
                  rows="3"
                  :class="inputClasses"
                  @input="updateExamen('description', $event.target.value)"
                  placeholder="Description détaillée de l'examen...">
        </textarea>
      </div>

      <!-- Date de réalisation -->
      <div>
        <label class="block text-sm text-gray-500 dark:text-gray-400 mb-1">
          Date de réalisation
        </label>
        <input v-model="examenData.date_realisation"
               type="date"
               :class="inputClasses"
               @input="updateExamen('date_realisation', $event.target.value)">
      </div>

      <!-- Urgence -->
      <div class="flex items-center">
        <input v-model="examenData.urgence"
               type="checkbox"
               id="urgence"
               class="mr-2"
               @change="updateExamen('urgence', $event.target.checked)">
        <label for="urgence" 
               class="text-sm"
               :class="theme === 'dark' ? 'text-gray-300' : 'text-gray-700'">
          Urgent
        </label>
      </div>
    </div>
  </div>

  <div class="space-y-6">
    <!-- Liste des examens -->
    <div class="space-y-4">
      <div v-for="(examen, index) in examens" :key="index" class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <USelect
            v-model="examen.type"
            :options="typesExamens"
            label="Type d'examen"
            required
          />
          <UInput
            v-model="examen.date_prevue"
            type="datetime-local"
            label="Date prévue"
            required
          />
        </div>
        
        <div class="mt-4">
          <UTextarea
            v-model="examen.details"
            label="Détails"
            placeholder="Précisions sur l'examen..."
            rows="2"
          />
        </div>

        <div class="mt-4 flex items-center justify-between">
          <UCheckbox
            v-model="examen.urgent"
            label="Urgent"
          />
          <UButton
            color="red"
            variant="soft"
            @click="removeExamen(index)"
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
        @click="addExamen"
        icon="i-heroicons-plus"
      >
        Ajouter un examen
      </UButton>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const emit = defineEmits(['update:modelValue', 'validate'])

const typesExamens = [
  { label: 'Analyse de sang', value: 'sang' },
  { label: 'Radiographie', value: 'radio' },
  { label: 'Échographie', value: 'echo' },
  { label: 'Scanner', value: 'scanner' },
  { label: 'IRM', value: 'irm' }
]

const examens = ref([])

const addExamen = () => {
  examens.value.push({
    type: '',
    date_prevue: '',
    details: '',
    urgent: false
  })
}

const removeExamen = (index) => {
  examens.value.splice(index, 1)
}

watch(examens, (newValue) => {
  emit('update:modelValue', newValue)
  emit('validate', examens.value.some(e => e.type && e.date_prevue))
}, { deep: true })

// Ajouter un premier examen vide au démarrage
addExamen()
</script>

<script>
export default {
  name: 'ExamenStep',

  props: {
    examenData: {
      type: Object,
      required: true
    },
    theme: {
      type: String,
      default: 'light'
    }
  },

  emits: ['update:examen-data', 'validate'],

  data() {
    return {
      typesExamen: [
        { label: 'Créatinine', value: 'Créatinine' },
        { label: 'DFU', value: 'DFU' },
        { label: 'Protéinurie', value: 'Protéinurie' },
        { label: 'Échographie rénale', value: 'Échographie' },
        { label: 'Autre', value: 'Autre' }
      ]
    }
  },

  computed: {
    inputClasses() {
      return [
        'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
        this.theme === 'dark' 
          ? 'bg-gray-700 border-gray-600 text-white' 
          : 'border-gray-300'
      ]
    },
    
    selectClasses() {
      return [
        'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
        this.theme === 'dark' 
          ? 'bg-gray-700 border-gray-600 text-white' 
          : 'border-gray-300'
      ]
    }
  },

  watch: {
    examenData: {
      handler(newVal) {
        // Vérifier si les données sont valides
        const isValid = this.validateData(newVal)
        this.$emit('validate', isValid)
      },
      immediate: true
    }
  },

  methods: {
    updateExamen(field, value) {
      const updatedExamen = { ...this.examenData }
      updatedExamen[field] = value
      this.$emit('update:examen-data', updatedExamen)
    },

    validateData(data) {
      // Logique de validation spécifique à l'étape
      return Object.keys(data).length > 0
    }
  }
}
</script>