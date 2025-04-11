<template>
  <div class="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
    <button 
      v-if="showBack"
      @click="$emit('back')"
      type="button"
      class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none"
    >
      Retour
    </button>
    
    <button 
      @click="$emit('cancel')"
      type="button"
      class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none"
    >
      Annuler
    </button>
    
    <button 
      @click="$emit('save')"
      type="button"
      :class="[
        'px-4 py-2 text-sm font-medium text-white rounded-md shadow-sm focus:outline-none',
        primaryButtonClass
      ]"
    >
      {{ saveLabel }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'ModalFooter',
  
  props: {
    showBack: {
      type: Boolean,
      default: false
    },
    saveLabel: {
      type: String,
      default: 'Enregistrer'
    },
    color: {
      type: String,
      default: 'blue'  // 'blue', 'green', 'red'
    }
  },

  emits: ['back', 'cancel', 'save'],

  computed: {
    primaryButtonClass() {
      const colors = {
        blue: 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800',
        green: 'bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-800',
        red: 'bg-red-600 hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-800'
      }
      return colors[this.color] || colors.blue
    }
  }
}
</script>