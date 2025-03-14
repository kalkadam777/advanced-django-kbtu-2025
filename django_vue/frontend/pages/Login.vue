<template>
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h1>Вход в аккаунт</h1>
                <p>Добро пожаловать! Пожалуйста, войдите в систему</p>
            </div>

            <form @submit.prevent="login" class="login-form">
                <div class="form-group" :class="{ error: error }">
                    <label for="username">Имя пользователя</label>
                    <div class="input-wrapper">
                        <i class="fa fa-user"></i>
                        <input
                            type="text"
                            id="username"
                            v-model="username"
                            placeholder="Введите имя пользователя"
                            required
                        />
                    </div>
                </div>

                <div class="form-group" :class="{ error: error }">
                    <label for="password">Пароль</label>
                    <div class="input-wrapper">
                        <i class="fa fa-lock"></i>
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            id="password"
                            v-model="password"
                            placeholder="Введите пароль"
                            required
                        />
                        <button
                            type="button"
                            class="toggle-password"
                            @click="showPassword = !showPassword"
                        >
                            <i
                                :class="
                                    showPassword
                                        ? 'fa fa-eye-slash'
                                        : 'fa fa-eye'
                                "
                            ></i>
                        </button>
                    </div>
                </div>

                <div class="error-message" v-if="error">
                    <i class="fa fa-exclamation-circle"></i> {{ error }}
                </div>

                <div class="remember-forgot">
                    <div class="remember-me">
                        <input
                            type="checkbox"
                            id="remember"
                            v-model="rememberMe"
                        />
                        <label for="remember">Запомнить меня</label>
                    </div>
                    <a href="#" class="forgot-password">Забыли пароль?</a>
                </div>

                <button type="submit" class="login-btn" :disabled="isLoading">
                    <span v-if="!isLoading">Войти</span>
                    <span v-else>
                        <i class="fa fa-spinner fa-spin"></i> Вход...
                    </span>
                </button>
            </form>

            <div class="alternate-auth">
                <p>
                    Нет аккаунта?
                    <router-link to="/register">Зарегистрироваться</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/store";

const router = useRouter();
const authStore = useAuthStore();

const username = ref("");
const password = ref("");
const rememberMe = ref(false);
const showPassword = ref(false);
const isLoading = ref(false);
const error = ref("");

const login = async () => {
    error.value = "";
    isLoading.value = true;

    try {
        await authStore.login(username.value, password.value);
        router.push("/admin");
    } catch (err) {
        error.value = "Неверное имя пользователя или пароль";
        console.error("Ошибка входа:", err);
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
}

.login-card {
    width: 100%;
    max-width: 450px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    padding: 40px;
}

.login-header {
    text-align: center;
    margin-bottom: 35px;
}

.login-header h1 {
    font-size: 28px;
    color: #333;
    margin-bottom: 10px;
    font-weight: 700;
}

.login-header p {
    color: #666;
    font-size: 16px;
}

.login-form {
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #333;
}

.input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.input-wrapper i {
    position: absolute;
    left: 15px;
    color: #999;
}

.form-group input[type="text"],
.form-group input[type="password"] {
    width: 100%;
    padding: 15px 15px 15px 45px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.3s;
}

.form-group input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.form-group.error input {
    border-color: #e53e3e;
}

.error-message {
    color: #e53e3e;
    font-size: 14px;
    margin: -10px 0 20px;
    display: flex;
    align-items: center;
}

.error-message i {
    margin-right: 6px;
}

.toggle-password {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    cursor: pointer;
    color: #999;
}

.toggle-password:focus {
    outline: none;
}

.remember-forgot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    font-size: 14px;
}

.remember-me {
    display: flex;
    align-items: center;
}

.remember-me input {
    margin-right: 8px;
}

.forgot-password {
    color: #667eea;
    text-decoration: none;
    transition: color 0.3s;
}

.forgot-password:hover {
    color: #5a6acf;
    text-decoration: underline;
}

.login-btn {
    width: 100%;
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 15px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 14px rgba(0, 0, 0, 0.1);
}

.login-btn:active {
    transform: translateY(0);
}

.login-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.alternate-auth {
    text-align: center;
    margin-top: 25px;
    color: #666;
}

.alternate-auth a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s;
}

.alternate-auth a:hover {
    color: #5a6acf;
    text-decoration: underline;
}

/* Для адаптивности */
@media (max-width: 576px) {
    .login-card {
        padding: 25px;
    }

    .login-header h1 {
        font-size: 24px;
    }

    .remember-forgot {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
}
</style>
