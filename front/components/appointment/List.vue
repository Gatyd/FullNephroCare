<script setup lang="ts">
import type { Appointment, Patient } from '~/types';

const emit = defineEmits(['update:modelValue'])

const props = defineProps({
    appointments: {
        type: Array as PropType<Appointment[]>,
        required: true,
    },
    modelValue: {
        type: Object as PropType<Appointment | null>,
        required: false,
    },
})

const selectedAppointment = computed({
    get() {
        return props.modelValue
    },
    set(value: Appointment | null) {
        emit('update:modelValue', value)
    }
})

const getHours = (date: Date) => {
    const options: Intl.DateTimeFormatOptions = { hour: "2-digit", minute: "2-digit" };
    return date.toLocaleString("fr-FR", options);
}

</script>
<template>
    <div class="p-0">
        <div v-for="(appoint, index) in appointments" :key="index">
            <div class="p-4 text-sm cursor-pointer border-l-2" :class="[
                selectedAppointment && selectedAppointment.id === appoint.id ? 'border-primary-500 dark:border-primary-400 bg-primary-100 dark:bg-primary-900/25' : 'border-white dark:border-gray-900 hover:border-primary-500/25 dark:hover:border-primary-400/25 hover:bg-primary-100/50 dark:hover:bg-primary-900/10'
            ]" @click="selectedAppointment = appoint">
                <div class="flex items-center justify-between font-semibold">
                    <div class="flex items-center gap-3">
                        {{ (appoint.patient as Patient).prenom }} {{ (appoint.patient as Patient).nom }}
                    </div>

                    <span>{{ getHours(new Date(appoint.date_prevue)) }}</span>
                </div>
                <p class="font-semibold">
                    {{ appoint.motif }}
                </p>
                <!-- <p class="text-gray-400 dark:text-gray-500 line-clamp-1">
                    {{ appoint.body }}
                </p> -->
            </div>
            <USeparator />
        </div>
    </div>
</template>