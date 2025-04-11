<template>
  <UModal v-model="isOpen" :ui="{ width: 'max-w-md' }">
    <UCard>
      <template #header>
        <div class="flex items-center space-x-2">
          <UIcon 
            :name="typeIcon" 
            class="text-2xl"
            :class="typeIconClass"
          />
          <h3 class="text-lg font-semibold">{{ title }}</h3>
        </div>
      </template>

      <p class="text-gray-600 dark:text-gray-300">
        {{ message }}
      </p>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <UButton
            @click="$emit('cancel')"
            variant="ghost"
          >
            Annuler
          </UButton>
          <UButton
            @click="$emit('confirm')"
            :color="type"
            :variant="type === 'danger' ? 'solid' : 'soft'"
          >
            Confirmer
          </UButton>
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  title: {
    type: String,
    default: 'Confirmation'
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'danger', 'warning'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const typeIcon = computed(() => {
  switch (props.type) {
    case 'danger': return 'i-heroicons-exclamation-triangle'
    case 'warning': return 'i-heroicons-exclamation-circle'
    default: return 'i-heroicons-question-mark-circle'
  }
})

const typeIconClass = computed(() => {
  switch (props.type) {
    case 'danger': return 'text-red-500'
    case 'warning': return 'text-yellow-500'
    default: return 'text-blue-500'
  }
})
</script>