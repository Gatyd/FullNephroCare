<template>
  <div 
    v-if="isVisible"
    class="flex items-center p-4 mb-4 rounded-lg"
    :class="typeClasses[type]"
  >
    <div class="flex-1">
      <span class="font-medium">{{ message }}</span>
    </div>
    <button 
      @click="close" 
      class="ml-3 -mx-1.5 -my-1.5 rounded-lg p-1.5 inline-flex h-8 w-8"
      :class="closeButtonClasses[type]"
    >
      <span class="sr-only">Fermer</span>
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'success', 'warning', 'error'].includes(value)
  },
  duration: {
    type: Number,
    default: 5000
  },
  autoClose: {
    type: Boolean,
    default: true
  }
})

const isVisible = ref(true)

const typeClasses = {
  info: 'text-blue-800 bg-blue-50 dark:bg-blue-900 dark:text-blue-300',
  success: 'text-green-800 bg-green-50 dark:bg-green-900 dark:text-green-300',
  warning: 'text-yellow-800 bg-yellow-50 dark:bg-yellow-900 dark:text-yellow-300',
  error: 'text-red-800 bg-red-50 dark:bg-red-900 dark:text-red-300'
}

const closeButtonClasses = {
  info: 'bg-blue-50 text-blue-500 hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-300 dark:hover:bg-blue-800',
  success: 'bg-green-50 text-green-500 hover:bg-green-200 dark:bg-green-900 dark:text-green-300 dark:hover:bg-green-800',
  warning: 'bg-yellow-50 text-yellow-500 hover:bg-yellow-200 dark:bg-yellow-900 dark:text-yellow-300 dark:hover:bg-yellow-800',
  error: 'bg-red-50 text-red-500 hover:bg-red-200 dark:bg-red-900 dark:text-red-300 dark:hover:bg-red-800'
}

const close = () => {
  isVisible.value = false
}

onMounted(() => {
  if (props.autoClose) {
    setTimeout(close, props.duration)
  }
})
</script>