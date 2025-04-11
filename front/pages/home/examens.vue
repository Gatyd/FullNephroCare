<script setup lang="ts">
  definePageMeta({
    scroll: false,
    middleware: 'home',
  })
  const links = [[{
    label: 'Examens',
    icon: 'i-heroicons-clipboard-document-check',
    to: '/home/examens/list/',
    exact: true
  }, {
    label: 'Résultats d\'examens',
    icon: 'i-heroicons-chart-bar',
    to: '/home/examens/resultats/',
  }, {
    label: 'Prescriptions',
    icon: 'i-heroicons-document-text',
    to: '/home/examens/prescriptions/',
  }]]
</script>

<template>
  <div class="flex flex-col h-full w-full pb-2">
 
    <UDashboardNavbar title="Examens" class="lg:text-2xl font-semibold flex-shrink-0" />
    
    <UDashboardToolbar class="py-0 px-1.5  overflow-x-auto">
      <UNavigationMenu :items="links" />
    </UDashboardToolbar>
    
 
    <div class="flex-1 overflow-hidden w-full">
      <NuxtPage class="h-full overflow-auto w-full" />
    </div>
  </div>
</template>
