<template>
  <div 
    v-if="show"
    :class="[
      'fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transform transition-transform duration-300',
      alertTypeClasses[type]
    ]"
  >
    <div class="flex items-center">
      <span class="mr-2">
        <Icon 
          :name="alertIcons[type]" 
          class="w-5 h-5"
        />
      </span>
      <span class="font-medium">{{ message }}</span>
      <button 
        @click="$emit('close')"
        class="ml-4 text-current hover:opacity-75"
      >
        <Icon name="i-heroicons-x-mark" class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'success',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  }
})

const emit = defineEmits(['close'])

const alertTypeClasses = {
  success: 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100',
  error: 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100',
  warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100',
  info: 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100'
}

const alertIcons = {
  success: 'i-heroicons-check-circle',
  error: 'i-heroicons-exclamation-circle',
  warning: 'i-heroicons-exclamation-triangle',
  info: 'i-heroicons-information-circle'
}
</script>