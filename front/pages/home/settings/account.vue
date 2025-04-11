<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '@nuxt/ui';
import { useUsersStore } from '~/store/userStore';

const toast = useToast()
const loading = ref(false)

const { user } = storeToRefs(useUsersStore());

console.log(user.value)

const state = reactive({
  last_name: user.value?.last_name || "",
  first_name: user.value?.first_name || "",
  email: user.value?.email || "",
})

const passwordState = reactive({
  current_password: "",
  password: "",
  confirm_password: "",
})

function validate(){
  const errors = [] as FormError[]
  if (!passwordState.current_password) errors.push({ name: 'current_password', message: 'Veuillez entrer le mot de passe actuel' })
  if (!passwordState.password) errors.push({ name: 'password', message: 'Veuillez entrer le nouveau mot de passe' })
  else if (passwordState.password.length < 8) errors.push({ name: 'password', message: 'Le mot de passe doit contenir au moins 8 caractères' })
  // else if (!/[A-Z]/.test(passwordState.password)) errors.push({ name: 'password', message: 'Le mot de passe doit contenir au moins une lettre majuscule' })
  // else if (!/[a-z]/.test(passwordState.password)) errors.push({ name: 'password', message: 'Le mot de passe doit contenir au moins une lettre minuscule' })
  // else if (!/[0-9]/.test(passwordState.password)) errors.push({ name: 'password', message: 'Le mot de passe doit contenir au moins un chiffre' })
  // else if (!/[^A-Za-z0-9]/.test(passwordState.password)) errors.push({ name: 'password', message: 'Le mot de passe doit contenir au moins un caractère spécial' })
  if (!passwordState.confirm_password) errors.push({ name: 'confirm_password', message: 'Veuillez confirmer le mot de passe' })
  if (passwordState.password !== passwordState.confirm_password) errors.push({ name: 'confirm_password', message: 'Les mots de passe ne correspondent pas' })
  return errors
}

function resetForm() {
  passwordState.current_password = ""
  passwordState.password = ""
  passwordState.confirm_password = ""
}

async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true
  const body = event.data
  const res = await apiRequest(
    () => $fetch(`/api/users/${user.value?.id}/`, {
      method: 'PATCH',
      credentials: "include",
      body: body,
    }),
    toast
  )
  if(res){
    resetForm()
    toast.add({
      icon: 'i-heroicons-check-circle',
      title: 'Mot de passe mis à jour',
      description: 'Votre mot de passe a été mis à jour avec succès',
      color: 'success',
    })
  }
  loading.value = false
}

</script>

<template>
  <div class="font-roboto mx-auto px-4 py-8">

    <div class="flex flex-col lg:flex-row gap-4 xl:gap-8 items-center">
      <UFormField label="Nom" name="last_name" class="w-full">
        <UInput class="w-full" v-model="state.last_name" disabled />
      </UFormField>
      <UFormField label="Prénom(s)" name="first_name" class="w-full">
        <UInput class="w-full" v-model="state.first_name" disabled />
      </UFormField>
      <UFormField label="Email" name="email" class="w-full">
        <UInput class="w-full" v-model="state.email" disabled />
      </UFormField>
    </div>

    <h3 class="text-base font-medium border-b border-gray-200 dark:border-gray-800 pb-2 mb-4 mt-8">
      Changer de mot de passe</h3>

    <UForm :state="passwordState" :validate="validate" @submit="onSubmit" class="space-y-4">
      <div class="flex flex-col lg:flex-row gap-4">
        <UFormField label="Mot de passe actuel" name="current_password" class="w-full">
          <UInput class="w-full" v-model="passwordState.current_password" />
        </UFormField>
        <UFormField label="Nouveau mot de passe" name="password" class="w-full">
          <UInput class="w-full" v-model="passwordState.password" />
        </UFormField>
        <UFormField label="Confirmation du mot de passe" name="confirm_password" class="w-full">
          <UInput class="w-full" v-model="passwordState.confirm_password" />
        </UFormField>
      </div>

      <div class="flex justify-end">
        <UButton :loading="loading" type="submit" label="Mettre à jour le mot de passe" />
      </div>
    </UForm>
  </div>
</template>