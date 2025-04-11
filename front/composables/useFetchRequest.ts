// ~/composables/useFetchRequest.ts
import { useUsersStore } from "~/store/userStore"

export async function useFetchRequest<T>(
  url: string,
  options?: any,
  toast?: any
) {
  const userStore = useUsersStore()

  const response = await useFetch<T>(url, options)

  // Si le token est expiré
  if (response.error.value?.statusCode === 401) {
    try {
      console.log("Tentative de refresh du token...")
      await userStore.refreshToken()

      // Retry après refresh
      const retryResponse = await $fetch<T>(url, options)
      console.log(retryResponse)

      return { data: retryResponse, status: "success" }
    } catch (refreshError) {
      console.error("Échec du rafraîchissement du token", refreshError)
      //return navigateTo("/login")
    }
  } else if (response.error.value) {
    toast && catchErrors(response.error.value, toast)
  }

  return response
}
