<script lang="ts" setup>
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'
import type { Row } from '@tanstack/vue-table'
import { getPaginationRowModel } from '@tanstack/vue-table'
import { useUsersStore } from "~/store/userStore";
import type { Patient } from "~/types";
import { upperFirst } from 'scule'
import getStadeColor from '~/utils/getStadeColor';

definePageMeta({
	middleware: "home"
})

const UButton = resolveComponent('UButton')
const UBadge = resolveComponent('UBadge')
const UDropdownMenu = resolveComponent('UDropdownMenu')

const patient = ref<Patient | undefined>(undefined)

const title = ref("")
const body = ref("")
const description = ref("")

const table = useTemplateRef('table')
const toast = useToast()
const q = ref("");
const formModal = ref(false)
const deleteModal = ref(false)
const textModal = ref(false)

const { data, status } = await useFetchRequest<Patient[]>('/api/patients/', {
	key: 'table-patients',
	lazy: true
})

function getRowItems(row: Row<Patient>) {
	return [
		{
			type: 'label',
			label: 'Actions'
		},
		{
			type: 'separator'
		},
		{
			label: 'Dossier complet',
			icon: 'i-heroicons-folder',
			onSelect() {
				navigator.clipboard.writeText(row.original.numero_dossier)

				toast.add({
					title: 'Payment ID copied to clipboard!',
					color: 'success',
					icon: 'i-lucide-circle-check'
				})
			}
		},
		{
			label: 'Modifier',
			icon: 'i-heroicons-pencil-square',
			onSelect() {
				patient.value = row.original
				formModal.value = true
			}
		},
		{
			label: 'Supprimer',
			color: 'error',
			icon: 'i-heroicons-trash',
			onSelect() {
				patient.value = row.original
				deleteModal.value = true
			}
		}
	]
}

const columns: TableColumn<Patient>[] = [
	{
		id: 'expand',
		cell: ({ row }) =>
			h(UButton, {
				color: 'neutral',
				variant: 'ghost',
				icon: 'i-lucide-chevron-down',
				square: true,
				'aria-label': 'Expand',
				ui: {
					leadingIcon: [
						'transition-transform',
						row.getIsExpanded() ? 'duration-200 rotate-180' : ''
					]
				},
				onClick: () => row.toggleExpanded()
			})
	},
	{
		accessorKey: 'numero_dossier',
		header: 'N° Dossier',
		cell: ({ row }) => {
			return row.getValue('numero_dossier')
		}
	},
	{
		accessorKey: 'nom',
		header: 'Nom',
		cell: ({ row }) => {
			return (row.getValue('nom') as string).split(" ")[0]
		}
	},
	{
		accessorKey: 'prenom',
		header: 'Prénom',
		cell: ({ row }) => {
			return (row.getValue('prenom') as string).split(" ")[0]
		}
	},
	{
		accessorKey: 'sexe',
		header: 'Sexe',
		cell: ({ row }) => {
			return row.getValue('sexe')
		}
	},
	{
		accessorKey: 'stade_mrc',
		header: ({ column }) => {
			const isSorted = column.getIsSorted()

			return h(UButton, {
				color: 'neutral',
				variant: 'ghost',
				label: 'Stade',
				icon: isSorted
					? isSorted === 'asc'
						? 'i-lucide-arrow-up-narrow-wide'
						: 'i-lucide-arrow-down-wide-narrow'
					: 'i-lucide-arrow-up-down',
				class: '-mx-2.5',
				onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
			})
		},
		cell: ({ row }) => {
			const color = getStadeColor(row.getValue('stade_mrc'))
			return h(UBadge, { class: 'capitalize', variant: 'subtle', color }, () =>
				row.getValue("stade_mrc") ? `Stade ${row.getValue('stade_mrc')}` : 'Pas malade'
			)
		}
	},
	{
		accessorKey: 'dfu',
		header: 'DFU', //(mL/min/1,73m²)
		cell: ({ row }) => {
			return row.getValue('dfu')
		}
	},
	{
		accessorKey: 'medecin_referent',
		header: 'Médecin Référent',
		cell: ({ row }) => {
			return `${(row.getValue('medecin_referent') as any).first_name} ${(row.getValue('medecin_referent') as any).last_name[0]}.`
		}
	},
	{
		accessorKey: 'date_creation',
		header: 'Enregistré le',
		cell: ({ row }) => {
			return formatDate(row.getValue('date_creation'), "short")
		}
	},
	{
		id: 'actions',
		cell: ({ row }) => {
			return h(
				'div',
				{ class: 'text-right' },
				h(
					UDropdownMenu,
					{
						content: {
							align: 'end'
						},
						items: getRowItems(row),
						'aria-label': 'Actions dropdown'
					},
					() =>
						h(UButton, {
							icon: 'i-lucide-ellipsis-vertical',
							color: 'neutral',
							variant: 'ghost',
							class: 'ml-auto',
							'aria-label': 'Actions dropdown'
						})
				)
			)
		}
	}
]

const expanded = ref({})

const pagination = ref({
	pageIndex: 0,
	pageSize: 10
})

async function onUpdatePatient(patient: Patient) {
	await refreshNuxtData('table-patients')
}

function openTextModal(modalTitle: string, modalBody: string, modalDescription: string) {
	title.value = modalTitle
	body.value = modalBody
	description.value = modalDescription
	textModal.value = true
}

</script>

<template>
	<PatientForm v-model="formModal" :patient="patient" @create="onUpdatePatient" @update="onUpdatePatient" />
	<PatientDelete v-model="deleteModal" v-if="patient" :patient="patient" @delete="onUpdatePatient" />
	<TextModal v-if="title" v-model="textModal" :title="title" :body="body" :description="description" />
	<UDashboardNavbar title="Patients" class="lg:text-2xl font-semibold" :ui="{ root: 'px-0' }">
		<template #trailing>
			<UBadge v-if="data?.length as number > 0" :label="data?.length" variant="subtle" />
		</template>
		<template #right>
			<UButton color="primary" label="Nouveau Patient" icon="i-heroicons-plus" class="mx-2"
				@click="patient = undefined; formModal = true" />
		</template>
	</UDashboardNavbar>
	<UDashboardToolbar>
		<template #left>
			<SearchInput v-model="q" />
		</template>

		<template #right>
			<UDropdownMenu :items="table?.tableApi
				?.getAllColumns()
				.filter((column) => column.getCanHide())
				.map((column) => ({
					label: upperFirst(column.id),
					type: 'checkbox' as const,
					checked: column.getIsVisible(),
					onUpdateChecked(checked: boolean) {
						table?.tableApi?.getColumn(column.id)?.toggleVisibility(!!checked)
					},
					onSelect(e?: Event) {
						e?.preventDefault()
					}
				}))
				" :content="{ align: 'end' }">
				<UButton label="Afficher" color="neutral" variant="outline" trailing-icon="i-lucide-chevron-down" />
			</UDropdownMenu>
		</template>
	</UDashboardToolbar>
	<div class="w-full space-y-4 pb-4">
		<UTable ref="table" v-model:expanded="expanded" :data="data as Patient[] | undefined" :columns="columns"
			v-model:global-filter="q" :ui="{ tr: 'data-[expanded=true]:bg-(--ui-bg-elevated)/50' }" class="flex-1"
			:loading="status === 'pending'" :pagination-options="{ getPaginationRowModel: getPaginationRowModel() }"
			v-model:pagination="pagination">
			<template #expanded="{ row }">
				<div class="flex justify-around">
					<div class="flex flex-col gap-2 w-1/3 xl:w-1/4 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Patient</h1>
						<p>Nom: <em class="font-semibold">{{ row.getValue("nom") }}</em></p>
						<p>Prénom: <em class="font-semibold">{{ row.getValue("prenom") }}</em></p>
						<p>Date de naissance: <em class="font-semibold">{{ formatDate(row.original.date_naissance,
							"long", false) }}</em></p>
						<p>Email: <em class="font-semibold">{{ row.original.email }}</em></p>
						<p>Téléphone: <em class="font-semibold">{{ row.original.telephone }}</em></p>
						<p class="whitespace-normal">
							Adresse: <em class="font-semibold break-words whitespace-pre-line">{{ row.original.adresse
							}}</em>
						</p>
					</div>

					<div class="flex flex-col gap-2 w-1/3 xl:w-1/4 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Informations médicales</h1>
						<p>Sexe: <em class="font-semibold">{{ row.getValue("sexe") }}</em></p>
						<p>Antécédants médicaux: <br>
							<UButton v-if="row.original.antecedents_medicaux" color="neutral" variant="subtle"
								icon="i-heroicons-document-text" class="mx-10 my-1"
								@click="openTextModal('Antécédants médicaux', row.original.antecedents_medicaux,
									`${row.original.nom} ${row.original.prenom}`
								)" />
							<em v-else class="font-semibold">Aucun antécéant médical</em>
						</p>
						<p>Allergies: <br>
							<UButton v-if="row.original.allergies" color="neutral" variant="subtle"
								icon="i-heroicons-document-text" class="mx-10 my-1"
								@click="openTextModal('Allergies', row.original.allergies,
									`${row.original.nom} ${row.original.prenom}`
								)" />
							<em v-else class="font-semibold">Aucune allergie</em>
						</p>
					</div>

					<div class="flex flex-col gap-2 w-1/3 xl:w-1/4 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Informations de suivi</h1>
						<p>Stade MRC:
							<UBadge :color="getStadeColor(row.getValue('stade_mrc'))" variant="subtle"
								:label="row.getValue('stade_mrc') ? `Stade ${row.getValue('stade_mrc')}` : 'Pas malade'"
								class="ms-3" />
						</p>
						<p>Débit de filtrage urinaire: <br> <em class="font-semibold">{{ row.getValue("dfu") }} mL / min
								/ 1,73m²</em></p>
						<p>Date d'enregistrement: <br><em class="font-semibold">{{
							formatDate(row.getValue("date_creation"), "long") }}</em></p>
						<p>Dernière modification: <br><em class="font-semibold">{{
							formatDate(row.original.date_modification, "long") }}</em></p>
					</div>

					<div class="hidden xl:flex flex-col gap-2 w-1/4 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Médecin Référent</h1>
						<p>Nom: <em class="font-semibold">{{ (row.getValue('medecin_referent') as any).first_name
						}}</em></p>
						<p>Prénom: <em class="font-semibold">{{ (row.getValue('medecin_referent') as any).last_name
						}}</em></p>
					</div>
				</div>
			</template>
		</UTable>

		<div
			class="flex flex-col md:flex-row justify-center gap-4 md:gap-0 items-center md:justify-between border-t border-(--ui-border) pt-4">
			<UFormField :ui="{ root: 'flex items-center' }" label="Lignes par page : ">
				<USelectMenu class="w-20 ms-3" :search-input="false" :items="[10, 20, 30, 40, 50]"
					v-model="pagination.pageSize" @update:model-value="(p) => table?.tableApi?.setPageSize(p)" />
			</UFormField>
			<UPagination :default-page="(table?.tableApi?.getState().pagination.pageIndex || 0) + 1"
				:items-per-page="table?.tableApi?.getState().pagination.pageSize"
				:total="table?.tableApi?.getFilteredRowModel().rows.length"
				@update:page="(p) => table?.tableApi?.setPageIndex(p - 1)" />
		</div>
	</div>

</template>
