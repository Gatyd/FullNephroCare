<script setup lang="ts">
import { navigateTo } from '#app'
import { UCard, UBadge } from '#components'
import type { Appointment } from '@/types'

const props = defineProps<{
  day: { date: Date; appointments: Appointment[] },
  isSelected: boolean
}>()

const today = new Date()
const isToday = (date: Date) => {
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

const isFuture = props.day.date > today
const isPast = props.day.date < today

const hasAppointments = computed(() => {
  return props.day.appointments.filter(a => a.statut === 'PLANIFIE').length > 0
})
const incompleteAppointments = props.day.appointments.filter(a => a.statut !== 'COMPLETE')

const bgColor = computed(() => {
  if (hasAppointments.value) {
    if (isToday(props.day.date)) {
      return 'bg-blue-500/20'
    } else if (isFuture && incompleteAppointments.length > 0) {
      return 'bg-green-500/20'
    } else if (isPast && incompleteAppointments.length > 0) {
      return 'bg-red-500/20'
    } else {
      return 'bg-muted/5'
    }
  } else {
    return 'bg-background'
  }
})

const borderColor = computed(() => {
  if (isToday(props.day.date)) {
    return 'border-2 border-blue-600 dark:border-blue-400'
  } else {
    return 'border border-gray-200 dark:border-gray-700'
  }
})

const goToDay = () => {
  const formatted = props.day.date.toLocaleDateString('fr-CA')
  navigateTo(`/home/appointments/${formatted}`)
}
</script>

<template>
  <UCard
    @click="goToDay"
    class="relative h-[100px] cursor-pointer transition-transform hover:scale-[1.02] duration-200"
    :class="[bgColor, isSelected ? 'ring-2 ring-primary' : '', borderColor]"
  >
    <template #header>
      <div class="flex items-center justify-between">
        <span class="font-semibold text-lg">{{ day.date.getDate() }}</span>
        <UBadge
          v-if="hasAppointments"
          variant="solid"
          size="sm"
          color="primary"
          class="text-xs px-2 py-0.5"
        >
          {{ props.day.appointments.filter(a => a.statut === 'PLANIFIE').length }}
        </UBadge>
      </div>
    </template>
  </UCard>
</template>
