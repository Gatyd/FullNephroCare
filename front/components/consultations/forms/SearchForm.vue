<template>
  <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md mb-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <h2 class="text-xl font-semibold text-blue-600 dark:text-blue-400 mb-4 md:mb-0">
        Rechercher une consultation
      </h2>
      <button @click="$emit('new-consultation')" 
              class="bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center">
        <span class="mr-2">+</span>Nouvelle consultation
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Input recherche patient -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Patient</label>
        <input 
          :value="searchPatient"
          @input="$emit('update:searchPatient', $event.target.value)"
          type="text" 
          placeholder="Rechercher un patient..." 
          class="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300"
        >
      </div>

      <!-- Select médecin -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Médecin</label>
        <select 
          :value="selectedMedecinId"
          @change="$emit('update:selectedMedecin', $event.target.value)"
          class="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300"
        >
          <option value="">Tous les médecins</option>
          <option v-for="medecin in medecins" :key="medecin.id" :value="medecin.id">
            {{ medecin.first_name }} {{ medecin.last_name }}
          </option>
        </select>
      </div>

      <!-- Inputs période -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Période</label>
        <div class="flex space-x-2">
          <input 
            :value="dateDebut"
            @input="$emit('update:dateDebut', $event.target.value)"
            type="date" 
            class="w-1/2 px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300"
          >
          <input 
            :value="dateFin"
            @input="$emit('update:dateFin', $event.target.value)"
            type="date"
            class="w-1/2 px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300"
          >
        </div>
      </div>
    </div>

    <div class="flex justify-end mt-4">
      <button @click="$emit('reset')" 
              class="px-4 py-2 bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-700 text-gray-800 dark:text-white rounded-md">
        Réinitialiser
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  searchPatient: String,
  selectedMedecinId: String,
  dateDebut: String,
  dateFin: String,
  medecins: {
    type: Array,
    required: true
  }
})

defineEmits([
  'update:searchPatient',
  'update:selectedMedecin',
  'update:dateDebut',
  'update:dateFin',
  'reset',
  'new-consultation'
])
</script>