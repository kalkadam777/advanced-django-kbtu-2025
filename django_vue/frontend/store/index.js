import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", () => {
    const token = ref(null);
    const user = ref(null);

    // Проверяем доступность localStorage перед использованием
    if (typeof window !== "undefined") {
        token.value = localStorage.getItem("token") || null;
        user.value = JSON.parse(localStorage.getItem("user")) || null;
    }

    const login = async (username, password) => {
        const response = await axios.post(
            "http://localhost:8000/api/token/",
            { username, password }, // Явно кодируем JSON
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        token.value = response.data.access;
        // user.value = response.data.user;

        if (typeof window !== "undefined") {
            localStorage.setItem("token", token.value);
            // localStorage.setItem('user', JSON.stringify(user.value));
        }
    };

    const logout = () => {
        token.value = null;
        // user.value = null;

        if (typeof window !== "undefined") {
            localStorage.removeItem("token");
            localStorage.removeItem("user");
        }
    };

    return {
        token,
        user,
        login,
        logout,
    };
});
