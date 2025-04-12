import { useUsersStore } from "~/store/userStore";

export default defineNuxtRouteMiddleware(async (to, from) => {
  // if (import.meta.server) return;
  const store = useUsersStore();
  if (!store.user) {
    const user = await store.getUser();
    if (!user) {
      const refreshedUser = await store.refreshToken();
      if (!refreshedUser) {
        return navigateTo("/login", { replace: true });
      }
    }
  }
});
