<template>
    <div class="register-container">
        <div class="register-card">
            <div class="register-header">
                <h1>Создать аккаунт</h1>
                <p>Заполните форму для регистрации</p>
            </div>

            <form @submit.prevent="register" class="register-form">
                <div class="form-group" :class="{ error: errors.username }">
                    <label for="username">Имя пользователя</label>
                    <div class="input-wrapper">
                        <i class="fa fa-user"></i>
                        <input
                            type="text"
                            id="username"
                            v-model="formData.username"
                            placeholder="Введите имя пользователя"
                            required
                        />
                    </div>
                    <span class="error-message" v-if="errors.username">{{
                        errors.username
                    }}</span>
                </div>

                <div class="form-group" :class="{ error: errors.email }">
                    <label for="email">Email</label>
                    <div class="input-wrapper">
                        <i class="fa fa-envelope"></i>
                        <input
                            type="email"
                            id="email"
                            v-model="formData.email"
                            placeholder="Введите ваш email"
                            required
                        />
                    </div>
                    <span class="error-message" v-if="errors.email">{{
                        errors.email
                    }}</span>
                </div>

                <div class="form-group" :class="{ error: errors.password }">
                    <label for="password">Пароль</label>
                    <div class="input-wrapper">
                        <i class="fa fa-lock"></i>
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            id="password"
                            v-model="formData.password"
                            placeholder="Создайте пароль"
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
                    <span class="error-message" v-if="errors.password">{{
                        errors.password
                    }}</span>
                </div>

                <div
                    class="form-group"
                    :class="{ error: errors.passwordConfirm }"
                >
                    <label for="passwordConfirm">Подтверждение пароля</label>
                    <div class="input-wrapper">
                        <i class="fa fa-lock"></i>
                        <input
                            :type="showConfirmPassword ? 'text' : 'password'"
                            id="passwordConfirm"
                            v-model="formData.passwordConfirm"
                            placeholder="Подтвердите пароль"
                            required
                        />
                        <button
                            type="button"
                            class="toggle-password"
                            @click="showConfirmPassword = !showConfirmPassword"
                        >
                            <i
                                :class="
                                    showConfirmPassword
                                        ? 'fa fa-eye-slash'
                                        : 'fa fa-eye'
                                "
                            ></i>
                        </button>
                    </div>
                    <span class="error-message" v-if="errors.passwordConfirm">{{
                        errors.passwordConfirm
                    }}</span>
                </div>

                <div class="form-group agree-terms">
                    <input
                        type="checkbox"
                        id="terms"
                        v-model="formData.agreeTerms"
                        required
                    />
                    <label for="terms"
                        >Я согласен с
                        <a href="#">правилами и условиями</a></label
                    >
                </div>

                <button
                    type="submit"
                    class="submit-btn"
                    :disabled="isSubmitting"
                >
                    <span v-if="!isSubmitting">Зарегистрироваться</span>
                    <span v-else>Регистрация...</span>
                </button>
            </form>

            <div class="alternate-auth">
                <p>
                    Уже есть аккаунт?
                    <router-link to="/login">Войти</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuthStore } from "~/store";

const router = useRouter();
const authStore = useAuthStore();

const formData = reactive({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
    agreeTerms: false,
});

const errors = reactive({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
});

const isSubmitting = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const validateForm = () => {
    let isValid = true;

    // Сбросить все ошибки
    Object.keys(errors).forEach((key) => {
        errors[key] = "";
    });

    // Проверка имени пользователя
    if (formData.username.length < 3) {
        errors.username =
            "Имя пользователя должно содержать не менее 3 символов";
        isValid = false;
    }

    // Проверка email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
        errors.email = "Введите корректный email адрес";
        isValid = false;
    }

    // Проверка пароля
    if (formData.password.length < 8) {
        errors.password = "Пароль должен содержать не менее 8 символов";
        isValid = false;
    }

    // Проверка подтверждения пароля
    if (formData.password !== formData.passwordConfirm) {
        errors.passwordConfirm = "Пароли не совпадают";
        isValid = false;
    }

    return isValid;
};

const register = async () => {
    if (!validateForm()) {
        return;
    }

    isSubmitting.value = true;

    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/api/register/",
            {
                username: formData.username,
                email: formData.email,
                password: formData.password,
            }
        );

        // Автоматический вход после регистрации
        await authStore.login(formData.username, formData.password);

        router.push("/");
    } catch (error) {
        if (error.response && error.response.data) {
            const responseErrors = error.response.data;

            if (responseErrors.username) {
                errors.username = responseErrors.username[0];
            }
            if (responseErrors.email) {
                errors.email = responseErrors.email[0];
            }
            if (responseErrors.password) {
                errors.password = responseErrors.password[0];
            }

            console.error("Ошибка регистрации:", error.response.data);
        } else {
            console.error("Ошибка регистрации:", error);
        }
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 20px;
}

.register-card {
    width: 100%;
    max-width: 500px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    padding: 40px;
}

.register-header {
    text-align: center;
    margin-bottom: 30px;
}

.register-header h1 {
    font-size: 28px;
    color: #333;
    margin-bottom: 10px;
}

.register-header p {
    color: #666;
    font-size: 16px;
}

.register-form {
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
.form-group input[type="email"],
.form-group input[type="password"] {
    width: 100%;
    padding: 12px 15px 12px 40px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.3s;
}

.form-group input:focus {
    outline: none;
    border-color: #4a90e2;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.form-group.error input {
    border-color: #e74c3c;
}

.error-message {
    color: #e74c3c;
    font-size: 14px;
    margin-top: 5px;
    display: block;
}

.toggle-password {
    position: absolute;
    right: 10px;
    background: none;
    border: none;
    cursor: pointer;
    color: #999;
}

.toggle-password:focus {
    outline: none;
}

.agree-terms {
    display: flex;
    align-items: center;
}

.agree-terms input {
    margin-right: 10px;
}

.agree-terms label {
    margin: 0;
    font-weight: normal;
}

.agree-terms a {
    color: #4a90e2;
    text-decoration: none;
}

.submit-btn {
    width: 100%;
    background-color: #4a90e2;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s;
}

.submit-btn:hover {
    background-color: #3a7bc8;
}

.submit-btn:disabled {
    background-color: #a0c3eb;
    cursor: not-allowed;
}

.alternate-auth {
    text-align: center;
    margin-top: 20px;
}

.alternate-auth p {
    color: #666;
}

.alternate-auth a {
    color: #4a90e2;
    text-decoration: none;
    font-weight: 600;
}

/* Для адаптивности */
@media (max-width: 576px) {
    .register-card {
        padding: 20px;
    }

    .register-header h1 {
        font-size: 24px;
    }
}
</style>
