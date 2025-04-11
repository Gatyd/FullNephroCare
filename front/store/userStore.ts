import { defineStore } from "pinia";
import type { LoginResponse, User } from "~/types";

export const useUsersStore = defineStore("users", {
  state: () => {
    return {
      user: null as User | null,
    };
  },

  actions: {
    async setUser(data: any, toast: any) {
      const res = await apiRequest(
        () =>
          $fetch(`/api/users/${this.user?.id}/`, {
            method: "PATCH",
            body: data,
            credentials: "include",
          }),
        toast
      );
      this.user = res;
    },

    async logoutUser() {
      try {
        await $fetch("/api/logout/", {
          method: "POST",
          credentials: "include",
        });
      } finally {
        this.user = null;
      }
    },

    async clearUser(toast: any) {
      await apiRequest(
        () =>
          $fetch(`/api/users/${this.user?.id}/`, {
            method: "DELETE",
            credentials: "include",
          }),
        toast
      );

      this.user = null;
    },

    async getUser() {
      try {
        const res = await $fetch(`/api/user/`, {
          credentials: "include",
        });
        if (res) {
          this.user = res;
          return res;
        }
      } catch (err: any) {
        this.user = null;
        return;
      }
    },

    async loginUser(credentials: any): Promise<LoginResponse> {
      try {
        const res = await $fetch("/api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: credentials,
          credentials: "include",
        });
        this.user = res;
        return { success: true, message: "Connecté avec succès" };
      } catch (err: any) {
        let errorMessage = "Identifiants de connexion invalides.";
        if (err.response) {
          const status = err.response.status;
          if (status >= 500) {
            errorMessage = "Erreur du serveur, réessayez plus tard.";
          } else if (status === 400) {
            errorMessage = "Identifiants de connexion invalides.";
          } 
        } else if (err.message) {
          errorMessage = "Problème de connexion au serveur.";
        }
        return { success: false, message: errorMessage };
      }
    },
    async refreshToken() {
      try {
        const data = await $fetch("/api/refresh/", {
          method: "POST",
          credentials: "include",
        });
        if (data) this.user = data;
        return data;
      } catch (error) {
        return null;
      }
    },
  },
});
