<template>
  <div class="flex justify-between items-center mb-6">
    <h3 class="text-lg font-medium text-gray-900 dark:text-white">
      {{ title }}
    </h3>
    <button 
      @click="$emit('close')"
      class="text-gray-400 hover:text-gray-500 focus:outline-none"
    >
      <span class="sr-only">Fermer</span>
      <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  name: 'ModalHeader',
  
  props: {
    title: {
      type: String,
      required: true
    }
  },

  emits: ['close']
}
</script>