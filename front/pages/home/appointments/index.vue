<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Appointment } from '@/types'

definePageMeta({
	middleware: "home"
})

const formModal = ref(false)

const appointment = ref<Appointment | undefined>(undefined)
const toast = useToast()
const isLoading = ref(true)

const appointments = ref<Appointment[]>([])
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const selectedDay = ref<{ date: Date; appointments: Appointment[] } | null>(null)

async function fetchAppointments() {
  appointments.value = await apiRequest<Appointment[]>(
    () => $fetch('/api/appointments/', {
      method: 'GET',
      credentials: "include"
    }),
    toast
  ) as Appointment[]
  isLoading.value = false
  console.log(appointments.value)
}

onMounted(fetchAppointments)

const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

const days = computed(() => {
  const lastDayOfMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  const dayList = []
  for (let i = 1; i <= lastDayOfMonth; i++) {
    const date = new Date(currentYear.value, currentMonth.value, i)
    const formatted = date.toLocaleDateString('fr-CA')
    const filtered = appointments.value.filter(app => {
      return new Date(app.date_prevue).toLocaleDateString('fr-CA') === formatted
    })
    dayList.push({ date, appointments: filtered })
  }
  return dayList
})

const isSelectedDay = (day: { date: Date }) => {
  return selectedDay.value?.date.toDateString() === day.date.toDateString()
}

const changeMonth = (dir: number) => {
  const newMonth = currentMonth.value + dir
  if (newMonth < 0) {
    currentMonth.value = 11
    currentYear.value--
  } else if (newMonth > 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value = newMonth
  }
}

const appointmentsOfMonth = computed(() => {
  return appointments.value.filter(a => {
    const date = new Date(a.date_prevue)
    return (
      date.getMonth() === currentMonth.value && 
      date.getFullYear() === currentYear.value &&
      a.statut !== 'COMPLETE'
    )
  }).length
})

</script>

<template>
  <AppointmentForm v-model="formModal" :appointment="appointment" @create="fetchAppointments" />
	<UDashboardNavbar title="Rendez-vous" class="lg:text-2xl font-semibold" :ui="{ root: 'px-0' }">
		<template #trailing>
			<UBadge v-if="appointmentsOfMonth" :label="appointmentsOfMonth" variant="subtle" />
		</template>
		<template #right>
			<UButton color="primary" label="Ajouter un rendez-vous" icon="i-heroicons-plus" class="mx-2"
				@click="appointment = undefined; formModal = true" />
		</template>
	</UDashboardNavbar>
  <div class="p-5 w-full flex justify-center">
    <div class="w-full max-w-7xl flex flex-col">
      <div class="flex items-center justify-between p-4">
        <UButton icon="i-heroicons-chevron-left" @click="changeMonth(-1)" />
        <span class="font-semibold text-xl">{{ monthNames[currentMonth] }} {{ currentYear }}</span>
        <UButton icon="i-heroicons-chevron-right" @click="changeMonth(1)" />
      </div>

      <div v-if="isLoading" class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-7 gap-4 p-4">
        <USkeleton v-for="i in 30" :key="i" class="h-[100px] rounded-xl" />
      </div>

      <div v-else class="grid grid-cols-3 md:grid-cols-5 xl:grid-cols-7 gap-4 p-4">
        <AppointmentDate
          v-for="(day, index) in days"
          :key="index"
          :day="day"
          :is-selected="isSelectedDay(day)"
        />
      </div>
    </div>
  </div>
</template>