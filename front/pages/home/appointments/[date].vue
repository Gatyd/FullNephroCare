<script setup lang="ts">
import type { Appointment } from '~/types';

const isLoading = ref(true)
const appointments = ref<Array<Appointment>>([])
const toast = useToast()
const formModal = ref(false)
const deleteModal = ref(false)
const route = useRoute()
const date = route.params.date
const formDate = ref(date as string | undefined)

const selectedAppointment = ref<Appointment | undefined>(undefined)

const isAppointmentPanelOpen = computed({
  get() {
    return !!selectedAppointment.value
  },
  set(value: boolean) {
    if (!value) {
      selectedAppointment.value = undefined
    }
  }
})

async function fetchAppointments() {
  appointments.value = await apiRequest<Appointment[]>(
    () => $fetch(`/api/appointments/?date=${date}`, {
      credentials: "include"
    }),
    toast
  ) as Appointment[]
  isLoading.value = false
  console.log(appointments.value)
}

function onEdit(){
  formDate.value = undefined;
  formModal.value = true
}

onMounted(() => {
  fetchAppointments()
})
</script>

<template>
  <AppointmentForm v-model="formModal" :date="formDate" :appointment="selectedAppointment" 
  @create="fetchAppointments" @update="fetchAppointments" />
  <AppointmentDelete v-if="selectedAppointment" v-model="deleteModal" :appointment="selectedAppointment" @delete="fetchAppointments" />

  <div class="flex flex-col md:flex-row">
    <UDashboardPanel id="appointments">
      <UDashboardNavbar title="Rendez-vous" class="lg:text-2xl font-semibold" :ui="{ root: 'px-0' }">
        <template #trailing>
          <UBadge v-if="appointments.length > 0" :label="appointments.length" variant="subtle" />
        </template>
        <template #right>
          <UButton color="primary" label="Ajouter un rendez-vous" icon="i-heroicons-plus" class="mx-2"
            @click="selectedAppointment = undefined; formModal = true; formDate = date as string | undefined" />
        </template>
      </UDashboardNavbar>

      <AppointmentList v-model="selectedAppointment" :appointments="appointments" />
    </UDashboardPanel>

    <UDashboardPanel v-model="isAppointmentPanelOpen" collapsible grow side="right">
      <template v-if="selectedAppointment">
        <AppointmentDetails :appointment="selectedAppointment" @edit="onEdit" @delete="deleteModal = true" />
      </template>
      <div v-else class="flex-1 hidden lg:flex items-center justify-center">
        <UIcon name="i-heroicons-calendar-days" class="w-32 h-32 text-gray-400 dark:text-gray-500" />
      </div>
    </UDashboardPanel>
  </div>
</template>
