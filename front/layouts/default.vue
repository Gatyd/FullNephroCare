<script setup lang="ts">
import NotificationChip from '~/components/NotificationChip.vue'
import Toast from '@/components/Toast.vue'

useSeoMeta({
    title: 'NephroCare Application',
    description: 'Gestion et suivi des données des patients atteints de maladie rénale chronique',
    robots: 'noindex, nofollow'
});

const logoutModal = ref(false)
const unreadNotifications = ref(5) // À voir avc le sytème de notifications

const links = [
    {
        id: "patients",
        label: "Patients",
        icon: "i-heroicons-user-group",
        to: "/home/patients",
        tooltip: {
            text: "Patients",
        },
    },
    {
        id: "consultations",
        label: "Consultations",
        icon: "i-heroicons-arrows-right-left",
        to: "/home/consultations",
        tooltip: {
            text: "Consultations",
        },
    },
    {
        id: "examens",
        label: "Examens",
        icon: "i-heroicons-document-text",
        defaultOpen: true,
        children: [
            {
                label: "Examens",
                to: "/home/examens/list",
            },
            {
                label: "Résultats d'examens",
                to: "/home/examens/resultats",
            },
            {
                label: "Prescriptions",
                to: "/home/examens/prescriptions",
            }
        ],
        tooltip: {
            text: "Examens",
        },
    },
    {
        id: "appointments",
        label: "Rendez-vous",
        icon: "i-heroicons-calendar-days",
        to: "/home/appointments",
        tooltip: {
            text: "Rendez-vous",
        },
    },
    {
        id: "notifications",
        label: "Notifications",
        icon: "i-heroicons-bell-alert",
        to: "/home/notifications",
        tooltip: {
            text: "Notifications",
        },
        trailing: () => unreadNotifications.value ? h(NotificationChip, {
            count: unreadNotifications.value
        }) : null
    },
    {
        id: "workflows",
        label: "Workflows",
        icon: "i-heroicons-arrow-path",
        to: "/home/workflows",
        tooltip: {
            text: "Workflows",
        },
    },
    {
        id: "settings",
        label: "Paramètres",
        defaultOpen: true,
        icon: "i-heroicons-cog-8-tooth",
        children: [
            {
                label: "Compte",
                to: "/home/settings/account",
            },
            {
                label: "Notifications",
                to: "/home/settings/notifications",
            },
            {
                label: "Workflows",
                to: "/home/settings/workflows",
            }
        ],
        tooltip: {
            text: "Paramètres",
        },
    },
];

const navigationMenuUi = {
    item: 'my-2'
}

const toast = ref({
  show: false,
  message: '',
  type: 'success'
})

const showToast = (message: string, type: string = 'success') => {
  toast.value = {
    show: true,
    message,
    type
  }
}

provide('showToast', showToast)
</script>

<template>

    <UDashboardGroup>
            <UDashboardSidebar collapsible resizable :min-size="14" :default-size="17.5" :max-size="21" :ui="{
                footer: 'block border-t border-(--ui-border)',
                header: 'lg:pt-10 lg:mb-4',
            }" toggle-side="right">
                <template #header="{ collapsed }">
                    <img src="/logo.png" alt="Logo NephroCare" :collapsed="collapsed" class="h-6 w-auto shrink-0" />
                    <h1 class=" lg:text-2xl font-bold text-primary-500 dark:text-white">NephroCare</h1>
                </template>

                <template #default="{ collapsed }">

                    <UNavigationMenu :collapsed="collapsed" :items="links" orientation="vertical"
                        :ui="navigationMenuUi" />

                    <div class="px-3 py-2 w-full mt-auto">
                        <UColorModeSelect class="w-full" />
                    </div>

                </template>

                <template #footer="{ collapsed }">
                    <div class="pb-2">
                        <UButton icon="i-heroicons-arrow-left-start-on-rectangle-16-solid" label="Déconnexion"
                            color="error" variant="ghost" class="w-full justify-start" @click="logoutModal = true" />
                    </div>
                </template>
            </UDashboardSidebar>

        <div
        class="relative lg:mt-6 lg:px-5 py-0 w-full overflow-auto"
        >
            <slot />
        </div>
        <Toast
          :show="toast.show"
          :message="toast.message"
          :type="toast.type"
          @close="toast.show = false"
        />
    </UDashboardGroup>
</template>