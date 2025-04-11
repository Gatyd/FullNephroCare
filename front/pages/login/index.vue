<script setup lang="ts">
import type { FormError } from "#ui/types";
import { useUsersStore } from "~/store/userStore";

definePageMeta({
    layout: false,
});

const error = ref("");
const store = useUsersStore();
const router = useRouter();

const fields = [
    {
        name: "email",
        type: "email",
        icon: "i-heroicons-envelope",
        required: true,
        // label: "Email",
        placeholder: "Entrez votre adresse email",
    },
    {
        name: "password",
        icon: "i-heroicons-lock-closed",
        required: true,
        // label: "Mot de passe",
        type: "password",
        placeholder: "Entrez votre mot de passe",
    },
];

const isValidEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

const validate = (state: any) => {
    const errors: FormError[] = [];
    if (!state.email)
        errors.push({ name: "email", message: "Adresse email obligatoire" });
    else if (!isValidEmail(state.email))
        errors.push({ name: "email", message: "Veuillez entrer un email valide" });
    if (!state.password)
        errors.push({ name: "password", message: "Mot de passe obligatoire" });
    return errors;
};

const loading = ref(false);

async function onSubmit(event: any) {
	loading.value = true
	const response = await store.loginUser(event.data);
	if (response.success) {
		router.push("/home/patients/")
	} else {
		error.value = response.message
		setTimeout(() => {
			error.value = ""
		}, 5000);
	}
	loading.value = false
}
</script>

<template>
    <div class="flex justify-center items-center h-screen bg-sky-50 dark:bg-gray-900">
        <UCard class="dark:bg-gray-800 mx-7 md:mx-0 w-full max-w-sm shadow-lg rounded-lg p-6">
            <a href="/">
                <img src="/public/logo.png" alt="NephroCare Logo" class="mx-auto mb-4 w-24 h-24" />
            </a>
            <UAuthForm :loading="loading" :fields="fields" :validate="validate" :providers="[]" title="Connexion!"
                :submitButton="{ label: 'Connexion', color: 'primary' }" @submit="onSubmit" :validate-on="['input','blur','change']">
                <template #title>
                    <h1 class="text-2xl font-bold text-primary dark:text-secondary font-poppins">Connexion</h1> 
                </template>
                <template #description>
                    <p class="text-gray-600 dark:text-gray-200 mt-2 font-roboto">Bienvenue sur notre plateforme<br>de suivi néphrologique !</p>
                </template>

                <template #validation>
                    <transition name="fade">
                        <UAlert v-if="error" color="error" icon="i-heroicons-information-circle-20-solid"
                            :title="error" />
                    </transition>
                </template>
            </UAuthForm>
        </UCard>
    </div>
</template>