<template>
  <div
    v-if="show"
    :class="[
      'fixed z-50 p-4 rounded-md shadow-lg',
      positionClasses,
      typeClasses[type]
    ]"
  >
    <div class="flex items-center">
      <span class="mr-2">
        <i :class="iconClasses[type]"></i>
      </span>
      <span>{{ message }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'success',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  position: {
    type: String,
    default: 'top-right'
  },
  message: {
    type: String,
    required: true
  }
})

const show = ref(false)

const positionClasses = computed(() => {
  switch (props.position) {
    case 'top-right':
      return 'top-4 right-4'
    case 'top-left':
      return 'top-4 left-4'
    case 'bottom-right':
      return 'bottom-4 right-4'
    case 'bottom-left':
      return 'bottom-4 left-4'
    default:
      return 'top-4 right-4'
  }
})

const typeClasses = {
  success: 'bg-green-500 text-white',
  error: 'bg-red-500 text-white',
  warning: 'bg-yellow-500 text-white',
  info: 'bg-blue-500 text-white'
}

const iconClasses = {
  success: 'i-heroicons-check-circle',
  error: 'i-heroicons-x-circle',
  warning: 'i-heroicons-exclamation-triangle',
  info: 'i-heroicons-information-circle'
}

const showToast = () => {
  show.value = true
  setTimeout(() => {
    show.value = false
  }, 3000)
}

defineExpose({
  showToast
})
</script>