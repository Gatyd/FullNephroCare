<script setup lang="ts">
import { h, resolveComponent, ref, computed } from 'vue'
import { upperFirst } from 'scule'
import type { TableColumn } from '@nuxt/ui'
import type { ResultatExamen } from "~/types";


const open = ref(false)
const q = ref("")
const openEditModal = ref(false)
const openDeleteModal = ref(false)
const UButton = resolveComponent('UButton')
const UCheckbox = resolveComponent('UCheckbox')
const UBadge = resolveComponent('UBadge')
const UDropdownMenu = resolveComponent('UDropdownMenu')
const formModal = ref(false)
const formUpdateModal = ref(false)
const resultat = ref<ResultatExamen | undefined>(undefined)



const patientInput = ref('')

const toast = useToast()


// Nouvel objet pour stocker le résultat d'examen en cours de modification
const currentResultat = ref<ResultatExamen>({
  id: 0,
  patient: 0,
  examen_prescrit: null,
  type_examen: '',
  date_realisation: '',
  laboratoire: '',
  resultats_texte: '',
  fichier_resultats: null,
  creatinine: null,
  dfu: null,
  proteinurie: null,
  interpretation: '',
  est_anormal: false,
  date_ajout: '',
  ajoute_par: null
})

const resultatToDeleteId = ref<number | null>(null)

// const data = ref<ResultatExamen[]>([
//   { id: 1, patient: 101, examen_prescrit: 1, type_examen: "IRM", date_realisation: "2024-03-10", laboratoire: "Centre Imagerie Médicale", resultats_texte: "Résultats normaux", fichier_resultats: "/files/irm_101.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Aucune anomalie détectée", est_anormal: false, date_ajout: "2024-03-01T10:00:00", ajoute_par: 5 },
//   { id: 2, patient: 102, examen_prescrit: 2, type_examen: "Radio", date_realisation: "2024-03-11", laboratoire: "Centre Imagerie Médicale", resultats_texte: "Légère anomalie", fichier_resultats: "/files/radio_102.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Légère opacité à droite", est_anormal: true, date_ajout: "2024-03-02T11:30:00", ajoute_par: 6 },
//   { id: 3, patient: 103, examen_prescrit: 3, type_examen: "Scanner", date_realisation: "2024-03-12", laboratoire: "Clinique Saint-Pierre", resultats_texte: "Résultats normaux", fichier_resultats: "/files/scanner_103.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Scanner normal", est_anormal: false, date_ajout: "2024-03-03T09:15:00", ajoute_par: 5 },
//   { id: 4, patient: 104, examen_prescrit: 4, type_examen: "Échographie", date_realisation: "2024-03-13", laboratoire: "Cabinet Dr. Petit", resultats_texte: "Voir détails en annexe", fichier_resultats: "/files/echo_104.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Anomalie détectée", est_anormal: true, date_ajout: "2024-03-04T14:45:00", ajoute_par: 7 },
//   { id: 5, patient: 105, examen_prescrit: 5, type_examen: "Analyse de sang", date_realisation: "2024-03-14", laboratoire: "Laboratoire Central", resultats_texte: "Résultats complets", fichier_resultats: "/files/sang_105.pdf", creatinine: 75, dfu: 120, proteinurie: 15, interpretation: "Valeurs normales", est_anormal: false, date_ajout: "2024-03-05T16:20:00", ajoute_par: 8 },
//   { id: 6, patient: 106, examen_prescrit: 6, type_examen: "Analyse d'urine", date_realisation: "2024-03-15", laboratoire: "Laboratoire Central", resultats_texte: "Résultats détaillés", fichier_resultats: "/files/urine_106.pdf", creatinine: 90, dfu: 110, proteinurie: 30, interpretation: "Protéinurie élevée", est_anormal: true, date_ajout: "2024-03-06T08:10:00", ajoute_par: 8 },
//   { id: 7, patient: 107, examen_prescrit: 7, type_examen: "IRM", date_realisation: "2024-03-16", laboratoire: "Hôpital Régional", resultats_texte: "Compte rendu complet", fichier_resultats: "/files/irm_107.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Anomalies multiples", est_anormal: true, date_ajout: "2024-03-07T12:50:00", ajoute_par: 9 },
//   { id: 8, patient: 108, examen_prescrit: 8, type_examen: "Scanner", date_realisation: "2024-03-17", laboratoire: "Clinique du Parc", resultats_texte: "Résultats normaux", fichier_resultats: "/files/scanner_108.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Aucune anomalie", est_anormal: false, date_ajout: "2024-03-08T10:30:00", ajoute_par: 5 },
//   { id: 9, patient: 109, examen_prescrit: 9, type_examen: "Analyse de sang", date_realisation: "2024-03-18", laboratoire: "Laboratoire Express", resultats_texte: "Résultats complets", fichier_resultats: "/files/sang_109.pdf", creatinine: 100, dfu: 90, proteinurie: 45, interpretation: "Valeurs hors normes", est_anormal: true, date_ajout: "2024-03-09T15:05:00", ajoute_par: 7 },
//   { id: 10, patient: 110, examen_prescrit: 10, type_examen: "Échographie", date_realisation: "2024-03-19", laboratoire: "Cabinet Dr. Martin", resultats_texte: "Voir annexe", fichier_resultats: "/files/echo_110.pdf", creatinine: null, dfu: null, proteinurie: null, interpretation: "Examen normal", est_anormal: false, date_ajout: "2024-03-10T18:00:00", ajoute_par: 6 }
// ]);
const deleteModal = ref(false)
const { data, status } = await useFetchRequest<ResultatExamen[]>('/api/resultats-examens/', {
	key: 'table-resultats',
	lazy: true
})
const filterQuery = ref('')

const columns: TableColumn<ResultatExamen>[] = [
  {
    accessorKey: 'patient',
    header: 'Patient',
    cell: ({ row }) => `Patient #${row.original.patient}`
  },
  {
    accessorKey: 'type_examen',
    header: 'Type d\'examen',
    cell: ({ row }) => row.original.type_examen
  },
  {
    accessorKey: 'laboratoire',
    header: 'Laboratoire',
    cell: ({ row }) => row.original.laboratoire || '-'
  },
  {
    accessorKey: 'date_realisation',
    header: 'Date de réalisation',
    cell: ({ row }) => row.original.date_realisation
  },
  {
    accessorKey: 'est_anormal',
    header: 'État',
    cell: ({ row }) => {
      const estAnormal = row.original.est_anormal
      return h(UBadge, { 
        variant: 'subtle', 
        color: estAnormal ? 'error' : 'success' 
      }, () => estAnormal ? 'Anormal' : 'Normal')
    }
  },
  {
    accessorKey: 'fichier_resultats',
    header: 'Fichier',
    cell: ({ row }) => row.original.fichier_resultats 
      ? h('a', { 
          href: row.original.fichier_resultats, 
          target: '_blank',
          class: 'text-blue-500 hover:underline flex items-center'
        }, [
        h('span', {
            class: 'iconify mr-1',
            'data-icon': 'lucide:eye',
            style: 'font-size: 1.2rem;',
          }),
          'Voir',
        ]) 
      : '-'
  },
  {
    accessorKey: 'date_ajout',
    header: 'Date d\'ajout',
    cell: ({ row }) => {
      return new Date(row.original.date_ajout).toLocaleString('fr-FR', {
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
      const items = [
      {
        type: 'label',
        label: 'Actions'
      },
      {
        label: row.getIsExpanded() ? 'Réduire' : 'Voir plus',
        icon: row.getIsExpanded() ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down',
        iconClass: ['text-sm','text-blue-500'],
        onSelect() {
          row.toggleExpanded()
        }
      },
      {
        type: 'separator'
      },
      {
        label: 'Modifier le résultat',
        icon: 'i-lucide-pen',
        onSelect() {
          resultat.value = row.original
          console.log(row.original)
				  formModal.value = true
        }
      },
      {
        label: 'Supprimer le résultat',
        icon: 'i-lucide-trash',
        iconClass: 'text-sm',
        onSelect() {
          resultat.value = row.original
				  deleteModal.value = true
        }
      }
    ]


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
async function refreshListResultats(resultat: ResultatExamen) {
	await refreshNuxtData('table-resultats')
}
const table = useTemplateRef('table')

</script>

<template>
  <ResultatForm v-model="formModal" :resultat="resultat" @create="refreshListResultats" @update="refreshListResultats"/>
  <ResultatDelete v-model="deleteModal" v-if="resultat" :resultat="resultat" @delete="refreshListResultats" />
  <div class="flex flex-col h-full">
    <div class="w-full border border-(--ui-border-accented) flex flex-col h-full overflow-hidden mb-5">
      <div class="flex items-center gap-2 px-4 py-3.5 overflow-x-auto">
        <SearchInput v-model="q" />
        <UButton color="primary" label="Ajouter un résultat" icon="i-heroicons-plus" class="mx-2"
				@click="resultat = undefined ; formModal = true" />
  
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

        <UTable ref="table" :data="data as ResultatExamen[] | undefined" :columns="columns" sticky class="h-full" v-model:global-filter="q" :loading="status === 'pending'">
          <template #expanded="{ row }">
            <div class="p-4 bg-gray-50 dark:bg-gray-800">
              <h3 class="text-lg font-medium mb-3 dark:text-white">Détails du résultat d'examen #{{ row.original.id }}</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Patient:</strong> #{{ row.original.patient }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Examen prescrit:</strong> {{ row.original.examen_prescrit ? `#${row.original.examen_prescrit}` : 'Non spécifié' }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Type d'examen:</strong> {{ row.original.type_examen }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Date de réalisation:</strong> {{ row.original.date_realisation }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">Laboratoire:</strong> {{ row.original.laboratoire || 'Non spécifié' }}</p>
                  <p class="dark:text-gray-200"><strong class="dark:text-white">État:</strong> <UBadge :color="row.original.est_anormal ? 'error' : 'success'" variant="subtle">{{ row.original.est_anormal ? 'Anormal' : 'Normal' }}</UBadge></p>
                </div>
                
                <div>
                  <p  class="dark:text-gray-200" v-if="row.original.creatinine !== null"><strong class="dark:text-white" >Créatinine:</strong> {{ row.original.creatinine }} µmol/L</p>
                  <p  class="dark:text-gray-200" v-if="row.original.dfu !== null"><strong class="dark:text-white" >DFU:</strong> {{ row.original.dfu }} ml/min</p>
                  <p  class="dark:text-gray-200" v-if="row.original.proteinurie !== null"><strong class="dark:text-white" >Protéinurie:</strong> {{ row.original.proteinurie }} mg/24h</p>
                  <p class="dark:text-gray-200" ><strong class="dark:text-white">Date d'ajout:</strong> {{ new Date(row.original.date_ajout).toLocaleString('fr-FR') }}</p>
                  <p class="dark:text-gray-200" ><strong class="dark:text-white">Ajouté par:</strong> {{ row.original.ajoute_par ? `Utilisateur #${row.original.ajoute_par}` : 'Non spécifié' }}</p>
                  <p  class="dark:text-gray-200" v-if="row.original.fichier_resultats"><strong class="dark:text-white" >Fichier:</strong> <a :href="row.original.fichier_resultats" target="_blank" class="text-blue-500 hover:underline">{{ row.original.fichier_resultats }}</a></p>
                </div>
              </div>
              
              <div class="mt-4">
                <h4 class="font-medium mb-2 dark:text-white">Résultats texte:</h4>
                <div class="bg-white dark:bg-gray-700 p-3 border dark:border-gray-600 rounded dark:text-gray-200">
                  {{ row.original.resultats_texte || 'Aucun texte disponible' }}
                </div>
              </div>
    
              <div class="mt-4">
                <h4 class="font-medium mb-2 dark:text-white">Interprétation:</h4>
                <div class="bg-white dark:bg-gray-700 p-3 border dark:border-gray-600 rounded dark:text-gray-200">
                  {{ row.original.interpretation || 'Aucune interprétation disponible' }}
                </div>
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