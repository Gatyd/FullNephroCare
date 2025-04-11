<template>
  <div v-if="modelValue" class="fixed inset-0 bg-black/75 dark:bg-black/90 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md mx-auto p-6">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold text-red-600 dark:text-red-400">
          Confirmation de suppression
        </h2>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100">
          &times;
        </button>
      </div>

      <!-- Content -->
      <div class="mb-6">
        <p class="text-gray-600 dark:text-gray-300">
          Êtes-vous sûr de vouloir supprimer {{ itemName }} ?
        </p>
        <p class="mt-2 text-sm text-red-500 dark:text-red-400">
          Cette action est irréversible.
        </p>
      </div>

      <!-- Footer -->
      <div class="flex justify-end space-x-3">
        <button 
          @click="closeModal"
          class="px-4 py-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100"
          :class="theme === 'dark' ? 'bg-gray-700 hover:bg-gray-800' : 'bg-gray-100 hover:bg-gray-200'"
        >
          Annuler
        </button>
        <button 
          @click="confirm"
          class="px-4 py-2 rounded-md text-white font-medium bg-red-600 hover:bg-red-700"
        >
          Supprimer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  itemName: {
    type: String,
    required: true
  },
  theme: {
    type: String,
    default: 'light'
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const closeModal = () => {
  emit('update:modelValue', false)
}

const confirm = () => {
  emit('confirm')
  closeModal()
}
</script>