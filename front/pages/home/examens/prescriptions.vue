<script setup lang="ts">
import { h, resolveComponent, ref, computed } from 'vue'
import { upperFirst } from 'scule'
import type { TableColumn } from '@nuxt/ui'
import type { Prescription } from "~/types";

const open = ref(false)
const openEditModal = ref(false)
const openDeleteModal = ref(false)
const UButton = resolveComponent('UButton')
const UCheckbox = resolveComponent('UCheckbox')
const UBadge = resolveComponent('UBadge')
const UDropdownMenu = resolveComponent('UDropdownMenu')
const formModal = ref(false)
const q = ref("")
const prescription = ref<Prescription | undefined>(undefined)
const deleteModal = ref(false)

const { data, status } = await useFetchRequest<Prescription[]>('/api/prescriptions/', {
	key: 'table-prescriptions',
	lazy: true
})

const consultationInput = ref('')

const toast = useToast()

// Variable pour stocker l'ID de la prescription à supprimer
const prescriptionToDeleteId = ref<number | null>(null)

const filterQuery = ref('')


// Fonction pour convertir une prescription
// const convertPrescription = (prescription: Prescription) => {
//   const index = data.value.findIndex(p => p.id === prescription.id)
//   if (index !== -1 && !prescription.est_convertie) {
//     data.value[index] = { 
//       ...prescription, 
//       est_convertie: true, 
//       date_conversion: new Date().toISOString() 
//     }
//     toast.add({
//       title: `Prescription #${prescription.id} convertie avec succès`,
//       color: 'success',
//       icon: 'i-lucide-check'
//     })
//   }
// }

const columns: TableColumn<Prescription>[] = [
  {
    accessorKey: 'consultation',
    header: 'Consultation',
    cell: ({ row }) => `#${row.original.consultation}`
  },
  {
    accessorKey: 'medicament',
    header: 'Médicament',
    cell: ({ row }) => row.original.medicament
  },
  {
    accessorKey: 'posologie',
    header: 'Posologie',
    cell: ({ row }) => row.original.posologie
  },
  {
    accessorKey: 'duree_traitement',
    header: 'Durée',
    cell: ({ row }) => `${row.original.duree_traitement} jour${row.original.duree_traitement > 1 ? 's' : ''}`
  },
  {
    accessorKey: 'est_convertie',
    header: 'Statut',
    cell: ({ row }) => {
      const estConvertie = row.original.est_convertie
      return h(UBadge, { 
        variant: 'subtle', 
        color: estConvertie ? 'success' : 'warning' 
      }, () => estConvertie ? 'Convertie' : 'En attente')
    }
  },
  {
    accessorKey: 'date_creation',
    header: 'Date de création',
    cell: ({ row }) => {
      return new Date(row.original.date_creation).toLocaleString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  {
    id: 'actions',
    enableHiding: false,
    cell: ({ row }) => {
      const items = [{
        type: 'label',
        label: 'Actions'
      }, 
      {
        label: row.getIsExpanded() ? 'Réduire' : 'Voir plus',
        icon: row.getIsExpanded() ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down',
        onSelect() {
          row.toggleExpanded()
        }
      }, {
        type: 'separator'
      }, {
        label: 'Modifier la prescription',
        icon: 'i-lucide-pen',
        onSelect() {
          prescription.value = row.original
          console.log(row.original)
				  formModal.value = true
        }
      }]

      // Ajouter l'option "Convertir" uniquement si la prescription n'est pas déjà convertie
      if (!row.original.est_convertie) {
        items.push({
          label: 'Convertir la prescription',
          icon: 'i-lucide-repeat',
          onSelect() {
            // convertPrescription(row.original)
          }
        })
      }

      items.push({
        label: 'Supprimer la prescription',
        icon: 'i-lucide-trash',
        onSelect() {
          prescription.value = row.original
				  deleteModal.value = true
        }
      })

      return h('div', { class: 'text-right' }, h(UDropdownMenu, {
        'content': {
          align: 'end'
        },
        items,
        'aria-label': 'Actions dropdown'
      }, () => h(UButton, {
        'icon': 'i-lucide-ellipsis-vertical',
        'color': 'neutral',
        'variant': 'ghost',
        'class': 'ml-auto',
        'aria-label': 'Actions dropdown'
      })))
    }
  }
]

async function refreshListPrescriptions(prescription: Prescription) {
	await refreshNuxtData('table-prescriptions')
}
const table = useTemplateRef('table')


</script>

<template>
  <PrescriptionForm v-model="formModal" :prescription="prescription" @create="refreshListPrescriptions" @update="refreshListPrescriptions"/>
  <PrescriptionDelete v-model="deleteModal" v-if="prescription" :prescription="prescription" @delete="refreshListPrescriptions" />

  <div class="flex flex-col h-full">
    <div class="w-full border border-(--ui-border-accented) flex flex-col h-full overflow-hidden mb-5">
      <div class="flex items-center gap-2 px-4 py-3.5 overflow-x-auto">
        <SearchInput v-model="q" />
        <UButton color="primary" label="Nouvelle prescription" icon="i-heroicons-plus" class="mx-2"
				@click="prescription = undefined ; formModal = true" />
        
        <UDropdownMenu
          :items="table?.tableApi?.getAllColumns().filter(column => column.getCanHide()).map(column => ({
            label: upperFirst(column.id),
            type: 'checkbox' as const,
            checked: column.getIsVisible(),
            onUpdateChecked(checked: boolean) {
              table?.tableApi?.getColumn(column.id)?.toggleVisibility(!!checked)
            },
            onSelect(e?: Event) {
              e?.preventDefault()
            }
          }))"
          :content="{ align: 'end' }"
        >
          <UButton
            label="Colonnes"
            color="neutral"
            variant="outline"
            trailing-icon="i-lucide-chevron-down"
            class="ml-auto"
            aria-label="Columns select dropdown"
          />
        </UDropdownMenu>
      </div>
      <div class="flex-1 overflow-auto relative">

        <UTable ref="table" :data="data as Prescription[] | undefined" :columns="columns" sticky class="h-full" v-model:global-filter="q" :loading="status === 'pending'">
          <template #expanded="{ row }">
            <div class="p-4 bg-gray-50 dark:bg-gray-800">
              <h3 class="text-lg font-medium mb-3 dark:text-white">Détails de la prescription #{{ row.original.id }}</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Consultation:</strong> #{{ row.original.consultation }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Médicament:</strong> {{ row.original.medicament }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Posologie:</strong> {{ row.original.posologie }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Durée du traitement:</strong> {{ row.original.duree_traitement }} jour(s)</p>
                </div>
                
                <div>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Statut:</strong> <UBadge :color="row.original.est_convertie ? 'success' : 'warning'" variant="subtle">{{ row.original.est_convertie ? 'Convertie' : 'En attente' }}</UBadge></p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Date de création:</strong> {{ new Date(row.original.date_creation).toLocaleString('fr-FR') }}</p>
                  <p v-if="row.original.est_convertie && row.original.date_conversion" class="dark:text-gray-200"><strong class="dark:text-white">Date de conversion:</strong> {{ new Date(row.original.date_conversion).toLocaleString('fr-FR') }}</p>
                </div>
              </div>
              
              <div class="mt-4">
                <h4 class="font-medium mb-2 dark:text-white">Instructions:</h4>
                <div class="bg-white dark:bg-gray-700 p-3 border dark:border-gray-600 rounded dark:text-gray-200">{{ row.original.instructions || 'Aucune instruction spécifique' }}</div>
              </div>
              
              <div class="mt-4" v-if="!row.original.est_convertie">
                <UButton
                  color="success"
                  label="Convertir cette prescription"
                  icon="i-lucide-check"
                  @click=""
                />
              </div>
            </div>
          </template>
        </UTable>
      </div>

      <div class="px-4 py-3.5 text-sm text-(--ui-text-muted)">
        {{ table?.tableApi?.getFilteredSelectedRowModel().rows.length || 0 }} sur
        {{ table?.tableApi?.getFilteredRowModel().rows.length || 0 }} ligne(s) sélectionnée(s).
      </div>
    </div>
  </div>
</template>