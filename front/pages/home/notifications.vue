<template>

  <UDashboardNavbar title="Notifications" class="lg:text-2xl font-semibold" :ui="{ root: 'px-0' }">
    <template #trailing>
      <UBadge v-if="notifications.length > 0" :label="notifications.length" variant="subtle" />
    </template>
    <template #right>
      <SearchInput v-model="searchQuery" />
    </template>
  </UDashboardNavbar>
  <div class="space-y-6 px-5 mt-6">

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
      <div class="md:col-span-1">
        <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">Type</label>
        <select v-model="selectedType"
          class="w-full h-10 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:ring-2 focus:ring-blue-500">
          <option value="">Tous les types</option>
          <option v-for="type in types" :key="type.id" :value="type.id">{{ type.label }}</option>
        </select>
      </div>

      <div class="md:col-span-2">
        <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">Période</label>
        <div class="flex gap-2">
          <input type="date" v-model="startDate"
            class="w-full h-10 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-100" />
          <input type="date" v-model="endDate"
            class="w-full h-10 px-2 text-sm rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-100" />
        </div>
      </div>

      <div class="md:col-span-1 flex justify-end">
        <button @click="resetFilters"
          class="h-10 px-4 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500">
          Réinitialiser
        </button>
      </div>
    </div>

    <div v-if="startDate && endDate" class="text-sm text-gray-600 dark:text-gray-300 mt-2">
      Notifications du {{ formatSimpleDate(startDate) }} au {{ formatSimpleDate(endDate) }}
    </div>

    <div class="bg-white dark:bg-gray-800 p-4 sm:p-6 rounded-xl shadow">
      <div class="space-y-4">
        <div v-for="notif in filteredNotifications" :key="notif.id" @click="toggleExpand(notif.id)"
          class="flex justify-between items-start p-4 border-l-4 rounded-lg shadow-sm cursor-pointer transition hover:bg-gray-100 dark:hover:bg-gray-700 group"
          :class="notifStyles[notif.type_notification]?.border">
          <div class="flex items-start gap-4">
            <div class="flex-shrink-0 rounded-full w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center"
              :class="notifStyles[notif.type_notification]?.iconBg">
              <UIcon :name="notifStyles[notif.type_notification]?.icon"
                class="w-5 h-5 text-gray-700 dark:text-gray-900" />
            </div>

            <div class="flex-1">
              <h3 class="font-semibold text-gray-900 dark:text-gray-100 group-hover:underline">{{ notif.titre }}</h3>
              <p ref="messageRefs" :ref="(el: any) => messageRefsMap[notif.id] = el"
                class="mt-1 text-sm text-gray-600 dark:text-gray-300 transition-all duration-200" :class="{
                  'line-clamp-2': !expandedIds.includes(notif.id),
                  'whitespace-pre-wrap': expandedIds.includes(notif.id)
                }">
                {{ notif.message }}
              </p>
              <div v-if="clampedIds.includes(notif.id)" class="mt-1">
                <button @click.stop="toggleExpand(notif.id)"
                  class="text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none">
                  {{ expandedIds.includes(notif.id) ? 'Lire moins' : 'Lire plus' }}
                </button>
              </div>
              <div class="mt-2 text-xs text-gray-500 dark:text-gray-400">{{ formatDate(notif.date_creation) }}</div>
            </div>
          </div>
        </div>

        <div v-if="filteredNotifications.length === 0" data-testid="empty-state"
          class="text-center text-gray-500 dark:text-gray-400">
          {{ notifications.length > 0 ? 'Aucune notification ne correspond à vos critères.' : 'Aucune notification disponible.' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue'
import { UIcon } from '#components'
import type { UserNotification } from '~/types'

definePageMeta({
  middleware: "home"
})

const selectedType = ref('')
const expandedIds = ref<number[]>([])
const clampedIds = ref<number[]>([])
const messageRefsMap = reactive({})
const notifications = ref<UserNotification[]>([])
const searchQuery = ref('')
const startDate = ref('')
const endDate = ref('')
const toast = useToast()

onMounted(() => {
  loadNotifications()
  checkClamped()
})

async function loadNotifications() {
  notifications.value = await apiRequest<UserNotification[]>(
    () => $fetch('/api/notifications/', {
      credentials: 'include'
    }),
    toast
  ) as UserNotification[]
}

const types = [
  { id: 'ALERTE', label: 'Alertes' },
  { id: 'RENDEZ_VOUS', label: 'Rappels de rendez-vous' }
]

const notifStyles = {
  ALERTE: {
    border: 'border-red-500',
    iconBg: 'bg-red-200 dark:bg-red-300',
    icon: 'i-heroicons-exclamation-circle'
  },
  RENDEZ_VOUS: {
    border: 'border-yellow-500',
    iconBg: 'bg-yellow-200 dark:bg-yellow-300',
    icon: 'i-heroicons-calendar-days'
  }
}

const filteredNotifications = computed(() => {
  let filtered = notifications.value
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    const searchTerms = query.split(' ').filter(term => term.length > 0)
    filtered = filtered.filter((notification: UserNotification) => {
      const titleMatch = notification.titre.toLowerCase().includes(query)
      const messageMatch = notification.message.toLowerCase().includes(query)
      const dateMatch = notification.date_creation.toLowerCase().includes(query)
      return titleMatch || messageMatch || dateMatch || searchTerms.some(term =>
        notification.titre.toLowerCase().includes(term) ||
        notification.message.toLowerCase().includes(term) ||
        notification.date_creation.toLowerCase().includes(term)
      )
    })
  }
  if (selectedType.value) {
    filtered = filtered.filter(n => n.type_notification === selectedType.value)
  }
  if (startDate.value && endDate.value) {
    filtered = filtered.filter(n => {
      const notifDate = new Date(n.date_creation)
      return notifDate >= new Date(startDate.value) && notifDate <= new Date(endDate.value)
    })
  }
  return filtered
})

function resetFilters() {
  searchQuery.value = ''
  selectedType.value = ''
  startDate.value = ''
  endDate.value = ''
}

function toggleExpand(id: number) {
  if (expandedIds.value.includes(id)) {
    expandedIds.value = expandedIds.value.filter(expandedId => expandedId !== id)
  } else {
    expandedIds.value.push(id)
  }
}

function checkClamped() {
  clampedIds.value = []
  nextTick(() => {
    for (const notif of notifications.value) {
      const el = messageRefsMap[notif.id]
      if (el && el.scrollHeight > el.clientHeight) {
        clampedIds.value.push(notif.id as never)
      }
    }
  })
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fr-FR', {
    dateStyle: 'long',
    timeStyle: 'short'
  }).format(date)
}

function formatSimpleDate(dateString: string) {
  return new Intl.DateTimeFormat('fr-FR', {
    dateStyle: 'long'
  }).format(new Date(dateString))
}
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
