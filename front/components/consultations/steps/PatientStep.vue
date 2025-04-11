<template>
  <div class="space-y-6">
    <div class="space-y-4">
      <!-- Type de patient -->
      <div class="flex items-center space-x-4">
        <label class="flex items-center">
          <input 
            type="radio" 
            v-model="patientType" 
            value="existing"
            class="form-radio text-blue-600"
          >
          <span class="ml-2">Patient existant</span>
        </label>
        <label class="flex items-center">
          <input 
            type="radio" 
            v-model="patientType" 
            value="new"
            class="form-radio text-blue-600"
            @change="redirectToPatients"
          >
          <span class="ml-2">Nouveau patient</span>
        </label>
      </div>

      <!-- Sélection patient existant -->
      <div v-if="patientType === 'existing'" class="space-y-4">
        <USelect
          v-model="selectedPatientId"
          :options="formattedPatients"
          placeholder="Sélectionner un patient"
          searchable
        />
      </div>
    </div>
  </div>
</template>

<script>
// Déplacer les données statiques hors du setup
export const defaultPatients = [
  { id: 1, nom: 'Dupont', prenom: 'Jean', date_naissance: '1980-05-15', sexe: 'M' },
  { id: 2, nom: 'Martin', prenom: 'Sophie', date_naissance: '1992-03-22', sexe: 'F' },
  { id: 3, nom: 'Bernard', prenom: 'Michel', date_naissance: '1975-11-08', sexe: 'M' },
  { id: 4, nom: 'Petit', prenom: 'Marie', date_naissance: '1988-07-30', sexe: 'F' },
  { id: 5, nom: 'Robert', prenom: 'Philippe', date_naissance: '1965-09-12', sexe: 'M' }
]
</script>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDefaultMedecins } from '~/composables/useMedecins'

const router = useRouter()
const { defaultMedecins } = useDefaultMedecins()

const props = defineProps({
  patients: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'validate'])

const patientType = ref('existing')
const selectedPatientId = ref(null)

// Sélectionner un patient aléatoire au démarrage
onMounted(() => {
  const randomIndex = Math.floor(Math.random() * defaultPatients.length)
  selectedPatientId.value = defaultPatients[randomIndex].id
})

const formattedPatients = computed(() => {
  const allPatients = [...defaultPatients, ...props.patients]
  return allPatients.map(patient => ({
    label: `${patient.nom} ${patient.prenom}`,
    value: patient.id
  }))
})

const redirectToPatients = () => {
  router.push('/home/patients?action=new')
}

const isValid = computed(() => {
  return patientType.value === 'existing' && !!selectedPatientId.value
})

watch([patientType, selectedPatientId], () => {
  if (patientType.value === 'existing') {
    emit('update:modelValue', { id: selectedPatientId.value, type: 'existing' })
    emit('validate', isValid.value)
  }
})


</script>