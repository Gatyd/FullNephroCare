<script setup lang="ts">
import { h, resolveComponent, ref, computed } from 'vue'
import { upperFirst } from 'scule'
import type { TableColumn } from '@nuxt/ui'
import type { Consultation, Examen } from "~/types";

const open = ref(false)
const UButton = resolveComponent('UButton')
const UBadge = resolveComponent('UBadge')
const UDropdownMenu = resolveComponent('UDropdownMenu')
const formModal = ref(false)
const q = ref("")
const examen = ref<Examen | undefined>(undefined)

const patientInput = ref('')

const toast = useToast()

const examenToDeleteId = ref<number | null>(null)
const deleteModal = ref(false)
const { data, status } = await useFetchRequest<Examen[]>('/api/examens/', {
	key: 'table-examens',
	lazy: true
})

const filterQuery = ref('')

const columns: TableColumn<Examen>[] = [
  {
    accessorKey: 'consultation',
    header: 'Consultation',
    cell: ({ row }) => (row.original.consultation as Consultation).id
  },
  {
    accessorKey: 'type_examen',
    header: 'Type d\'examen',
    cell: ({ row }) => row.original.type_examen
  },
  {
    accessorKey: 'description',
    header: 'Description',
    cell: ({ row }) => row.original.description || '-'
  },
  {
    accessorKey: 'date_realisation',
    header: 'Date de réalisation',
    cell: ({ row }) => row.original.date_realisation
  },
  {
    accessorKey: 'urgence',
    header: 'Urgence',
    cell: ({ row }) => {
      const isUrgent = row.original.urgence
      return h(UBadge, { 
        variant: 'subtle', 
        color: isUrgent ? 'error' : 'neutral' 
      }, () => isUrgent ? 'Urgent' : 'Normal')
    }
  },
  {
    accessorKey: 'resultat',
    header: 'Résultat',
    cell: ({ row }) => row.original.resultat ? `#${row.original.resultat}` : 'En attente'
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
        color: 'info',
        icon: row.getIsExpanded() ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down',
        onSelect() {
          row.toggleExpanded()
        }
      }, {
        type: 'separator'
      }, {
        label: 'Modifier l\'examen',
        color: 'warning',
        icon: 'i-lucide-pen',
        onSelect() {
          examen.value = row.original
          console.log(row.original)
				  formModal.value = true
        }
      }, {
        label: 'Supprimer l\'examen',
        color: 'error',
        icon: 'i-lucide-trash',
        onSelect() {
          examen.value = row.original
				  deleteModal.value = true
        }
      }]

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

async function refreshListExamens(examen: Examen) {
	await refreshNuxtData('table-examens')
}

const table = useTemplateRef('table')

</script>

<template>
  <ExamenForm v-model="formModal" :examen="examen" @create="refreshListExamens" @update="refreshListExamens"/>
  <ExamenDelete v-model="deleteModal" v-if="examen" :examen="examen" @delete="refreshListExamens" />
  <div class="flex flex-col h-full">
    <div class="w-full border border-(--ui-border-accented) flex flex-col h-full overflow-hidden mb-5 pb-2">
      <div class="flex items-center gap-2 px-4 py-3.5 overflow-x-auto">
        <SearchInput v-model="q" />
        <UButton color="primary" label="Nouveau Examen" icon="i-heroicons-plus" class="mx-2"
				@click="examen = undefined ; formModal = true" />

  
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
      
      <!-- Zone du tableau avec défilement -->
      <div class="flex-1 overflow-auto relative">
        <UTable ref="table" :data="data as Examen[] | undefined" :columns="columns" sticky class="h-full" v-model:global-filter="q" :loading="status === 'pending'">
          <template #expanded="{ row }">
            <div class="p-4 bg-gray-50 dark:bg-gray-800">
              <h3 class="text-lg font-medium mb-3 dark:text-white">Détails du résultat d'examen #{{ row.original.id }}</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Patient:</strong> #{{ row.original.consultation }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Type d'examen:</strong> {{ row.original.type_examen }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Description:</strong> {{ row.original.description}}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Urgence:</strong> <UBadge :color="row.original.urgence ? 'error' : 'success'" variant="subtle">{{ row.original.urgence ? 'Urgent' : 'Normal' }}</UBadge></p>
                </div>
                
                <div>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Date de réalisation:</strong> {{ row.original.date_realisation }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Date de création:</strong> {{ row.original.date_creation}}</p>
                </div>
              </div>
            </div>
          </template>
        </UTable>
      </div>
    </div>
  </div>
</template>
