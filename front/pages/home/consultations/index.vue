<script lang="ts" setup>
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'
import type { Row } from '@tanstack/vue-table'
import { getPaginationRowModel } from '@tanstack/vue-table'
import { useUsersStore } from "~/store/userStore";
import type { Consultation, Patient } from "~/types";
import { upperFirst } from 'scule'
import getStadeColor from '~/utils/getStadeColor';

definePageMeta({
	middleware: "home"
})

const UButton = resolveComponent('UButton')
const UBadge = resolveComponent('UBadge')
const UDropdownMenu = resolveComponent('UDropdownMenu')

const consultation = ref<Consultation | undefined>(undefined)

const title = ref("")
const body = ref("")
const description = ref("")

const table = useTemplateRef('table')
const toast = useToast()
const q = ref("");
const formModal = ref(false)
const deleteModal = ref(false)
const textModal = ref(false)

const { data, status } = await useFetchRequest<Consultation[]>('/api/consultations/', {
	key: 'table-consultations',
	lazy: true
})

function getRowItems(row: Row<Consultation>) {
	return [
		{
			type: 'label',
			label: 'Actions'
		},
		{
			type: 'separator'
		},
		{
			label: 'Modifier',
			icon: 'i-heroicons-pencil-square',
			onSelect() {
				consultation.value = row.original
				formModal.value = true
			}
		},
		{
			label: 'Supprimer',
			color: 'error',
			icon: 'i-heroicons-trash',
			onSelect() {
				consultation.value = row.original
				deleteModal.value = true
			}
		}
	]
}

const columns: TableColumn<Consultation>[] = [
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
		accessorKey: 'date',
		header: 'Date',
		cell: ({ row }) => {
			return formatDate(row.getValue('date'), "short")
		}
	},
	{
		accessorKey: 'patient',
		header: 'Patient',
		cell: ({ row }) => {
			return `${(row.getValue('patient') as Patient).nom} ${(row.getValue('patient') as Patient).prenom[0]}.`
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
			const color = getStadeColor((row.getValue('patient') as Patient).stade_mrc)
			return h(UBadge, { class: 'capitalize', variant: 'subtle', color }, () =>
				(row.getValue('patient') as Patient).stade_mrc ? `Stade ${(row.getValue('patient') as Patient).stade_mrc}` : 'Pas malade'
			)
		}
	},
	{
		accessorKey: 'type_consultation',
		header: 'Type de consultation',
		cell: ({ row }) => {
			return row.getValue('type_consultation')
		}
	},
	{
		accessorKey: 'medecin',
		header: 'Médecin',
		cell: ({ row }) => {
			return `${(row.getValue('medecin') as any).first_name} ${(row.getValue('medecin') as any).last_name[0]}.`
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

async function onUpdateConsultation(consultation: Consultation) {
	await refreshNuxtData('table-consultations')
}

function openTextModal(modalTitle: string, modalBody: string, modalDescription: string) {
	title.value = modalTitle
	body.value = modalBody
	description.value = modalDescription
	textModal.value = true
}

</script>

<template>
	<ConsultationForm v-model="formModal" :consultation="consultation" @create="onUpdateConsultation"
		@update="onUpdateConsultation" />
	<ConsultationDelete v-model="deleteModal" v-if="consultation" :consultation="consultation"
		@delete="onUpdateConsultation" />
	<TextModal v-if="title" v-model="textModal" :title="title" :body="body" :description="description" />
	<UDashboardNavbar title="Consultations" class="lg:text-2xl font-semibold" :ui="{ root: 'px-0' }">
		<template #trailing>
			<UBadge v-if="data?.length as number > 0" :label="data?.length" variant="subtle" />
		</template>
		<template #right>
			<UButton color="primary" label="Nouvelle consultation" icon="i-heroicons-plus" class="mx-2"
				@click="consultation = undefined; formModal = true" />
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
		<UTable ref="table" v-model:expanded="expanded" :data="data as Consultation[] | undefined" :columns="columns"
			v-model:global-filter="q" :ui="{ tr: 'data-[expanded=true]:bg-(--ui-bg-elevated)/50' }" class="flex-1"
			:loading="status === 'pending'" :pagination-options="{ getPaginationRowModel: getPaginationRowModel() }"
			v-model:pagination="pagination">
			<template #expanded="{ row }">
				<div class="flex justify-around">
					<div class="flex flex-col gap-2 w-1/3 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Patient</h1>
						<p>Nom: <em class="font-semibold">{{ row.original.patient.nom }}</em></p>
						<p>Prénom: <em class="font-semibold">{{ row.original.patient.prenom }}</em></p>
						<p>Date de naissance: <em class="font-semibold">{{
							formatDate(row.original.patient.date_naissance,
								"long", false) }}</em></p>
						<p>Email: <em class="font-semibold">{{ row.original.patient.email }}</em></p>
						<p>Téléphone: <em class="font-semibold">{{ row.original.patient.telephone }}</em></p>
						<p class="whitespace-normal">
							Adresse: <em class="font-semibold break-words whitespace-pre-line">{{
								row.original.patient.adresse
							}}</em>
						</p>
					</div>

					<div class="flex flex-col gap-2 w-1/3 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Consultation</h1>
						<p>Date: <em class="font-semibold">{{ formatDate(row.original.date, "long", false) }}</em></p>
						<p>Type de consultation: <em class="font-semibold">{{ row.original.type_consultation }}</em></p>
						<p>Symptomes: <br>
							<UButton color="neutral" variant="subtle" icon="i-heroicons-document-text"
								class="mx-10 my-1" @click="openTextModal('Symptomes', row.original.symptomes,
									`${row.original.patient.nom} ${row.original.patient.prenom}`
								)" />
						</p>
						<p>Diagnostic: <br>
							<UButton v-if="row.original.diagnostic" color="neutral" variant="subtle"
								icon="i-heroicons-document-text" class="mx-10 my-1" @click="openTextModal('Diagnostic', row.original.diagnostic,
									`${row.original.patient.nom} ${row.original.patient.prenom}`
								)" />
							<em v-else class="font-semibold">Aucun diagnostic</em>
						</p>
					</div>

					<div class="flex flex-col gap-2 w-1/3 min-w-0 px-2">
						<h1 class="font-semibold text-base underline underline-offset-4">Médecin</h1>
						<p>Nom: <em class="font-semibold">{{ row.original.medecin.first_name }}</em></p>
						<p>Prénom: <em class="font-semibold">{{ row.original.medecin.last_name }}</em></p>
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
