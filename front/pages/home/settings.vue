<script setup lang="ts">

definePageMeta({
	middleware: "home"
})

const links = [[{
    label: 'Compte',
    icon: 'i-heroicons-user-circle',
    to: '/home/settings/account',
    exact: true
  }, {
    label: 'Notifications',
    icon: 'i-heroicons-bell-alert',
    to: '/home/settings/notifications'
  }, {
    label: 'Workflows',
    icon: 'i-heroicons-arrow-path',
    to: '/home/settings/workflows'
  }
]]

</script>

<template>
      <UDashboardNavbar title="Paramètres" class="lg:text-2xl font-semibold" />

      <UDashboardToolbar class="py-0 px-1.5 overflow-x-auto">
        <UNavigationMenu :items="links" />
      </UDashboardToolbar>

      <NuxtPage />
</template>
