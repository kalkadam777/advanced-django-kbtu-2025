<template>
    <div class="admin-layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>Admin Panel</h2>
            </div>
            <nav class="sidebar-nav">
                <ul>
                    <li class="active">
                        <i class="fas fa-tachometer-alt"></i>
                        <span>Дашборд</span>
                    </li>
                    <li>
                        <i class="fas fa-box"></i>
                        <span>Товары</span>
                    </li>
                    <li>
                        <i class="fas fa-users"></i>
                        <span>Пользователи</span>
                    </li>
                    <li>
                        <i class="fas fa-cog"></i>
                        <span>Настройки</span>
                    </li>
                </ul>
            </nav>
            <div class="sidebar-footer">
                <button @click="logout" class="logout-btn">
                    <i class="fas fa-sign-out-alt"></i>
                    <span>Выйти</span>
                </button>
            </div>
        </aside>

        <main class="content">
            <header class="content-header">
                <div class="search-bar">
                    <i class="fas fa-search"></i>
                    <input
                        type="text"
                        placeholder="Поиск..."
                        v-model="searchQuery"
                        @input="filterItems"
                    />
                </div>
                <div class="user-menu">
                    <span class="user-name">Администратор</span>
                    <div class="user-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                </div>
            </header>

            <div class="content-body">
                <div class="page-header">
                    <h1>Управление товарами</h1>
                    <button class="add-btn" @click="showAddForm = !showAddForm">
                        <i class="fas fa-plus"></i> Добавить товар
                    </button>
                </div>

                <div v-if="showAddForm" class="add-form-container">
                    <form @submit.prevent="addItem" class="add-form">
                        <h3>Добавить новый товар</h3>

                        <div class="form-group">
                            <label for="name">Название</label>
                            <input
                                type="text"
                                id="name"
                                v-model="newItem.name"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label for="description">Описание</label>
                            <textarea
                                id="description"
                                v-model="newItem.description"
                                required
                            ></textarea>
                        </div>

                        <div class="form-actions">
                            <button
                                type="button"
                                @click="showAddForm = false"
                                class="cancel-btn"
                            >
                                Отмена
                            </button>
                            <button type="submit" class="submit-btn">
                                <i class="fas fa-save"></i> Сохранить
                            </button>
                        </div>
                    </form>
                </div>

                <div class="items-container">
                    <div v-if="loading" class="loading">
                        <i class="fas fa-spinner fa-spin"></i>
                        <span>Загрузка данных...</span>
                    </div>

                    <div
                        v-else-if="filteredItems.length === 0"
                        class="no-items"
                    >
                        <i class="fas fa-info-circle"></i>
                        <p>Нет доступных товаров</p>
                    </div>

                    <div v-else class="items-table-container">
                        <table class="items-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Название</th>
                                    <th>Описание</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="item in filteredItems"
                                    :key="item.id"
                                >
                                    <td>{{ item.id }}</td>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.description }}</td>
                                    <td>
                                        <div class="actions">
                                            <button
                                                @click="editItem(item)"
                                                class="edit-btn"
                                            >
                                                <i class="fas fa-edit"></i>
                                            </button>
                                            <button
                                                @click="confirmDelete(item.id)"
                                                class="delete-btn"
                                            >
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>

        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal">
                <h3>Подтверждение удаления</h3>
                <p>Вы действительно хотите удалить этот элемент?</p>
                <div class="modal-actions">
                    <button @click="showDeleteModal = false" class="cancel-btn">
                        Отмена
                    </button>
                    <button @click="deleteSelectedItem" class="confirm-btn">
                        Удалить
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/store";
import axios from "axios";

const router = useRouter();
const authStore = useAuthStore();
const items = ref([]);
const loading = ref(true);
const searchQuery = ref("");
const showAddForm = ref(false);
const showDeleteModal = ref(false);
const selectedItemId = ref(null);

const newItem = ref({
    name: "",
    description: "",
});

const filteredItems = computed(() => {
    if (!searchQuery.value) return items.value;

    const query = searchQuery.value.toLowerCase();
    return items.value.filter(
        (item) =>
            item.name.toLowerCase().includes(query) ||
            item.description.toLowerCase().includes(query)
    );
});

const logout = () => {
    authStore.logout();
    router.push("/login");
};

const filterItems = () => {
    // Функция вызывается автоматически при вводе в поле поиска
    // Фильтрация происходит через computed свойство
};

const deleteItem = async (id) => {
    try {
        await axios.delete(`http://127.0.0.1:8000/api/items/${id}/`, {
            headers: { Authorization: `Bearer ${authStore.token}` },
        });
        items.value = items.value.filter((item) => item.id !== id);
    } catch (error) {
        console.error("Ошибка при удалении элемента:", error);
    }
};

const confirmDelete = (id) => {
    selectedItemId.value = id;
    showDeleteModal.value = true;
};

const deleteSelectedItem = async () => {
    if (selectedItemId.value) {
        await deleteItem(selectedItemId.value);
        showDeleteModal.value = false;
        selectedItemId.value = null;
    }
};

const addItem = async () => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/api/items/",
            newItem.value,
            {
                headers: { Authorization: `Bearer ${authStore.token}` },
            }
        );
        items.value.push(response.data);
        newItem.value = { name: "", description: "" };
        showAddForm.value = false;
    } catch (error) {
        console.error("Ошибка при добавлении элемента:", error);
    }
};

const editItem = (item) => {
    // Здесь можно реализовать функцию редактирования
    // Например, открыть модальное окно с формой редактирования
    console.log("Редактирование элемента", item);
};

onMounted(async () => {
    try {
        loading.value = true;
        const response = await axios.get("http://127.0.0.1:8000/api/items/", {
            headers: { Authorization: `Bearer ${authStore.token}` },
        });
        items.value = response.data;
    } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
    } finally {
        loading.value = false;
    }
});
</script>

<style scoped>
.admin-layout {
    display: flex;
    min-height: 100vh;
    background-color: #f5f7fb;
}

/* Боковая панель */
.sidebar {
    width: 250px;
    background-color: #2c3e50;
    color: #fff;
    display: flex;
    flex-direction: column;
}

.sidebar-header {
    padding: 20px;
    border-bottom: 1px solid #3c546c;
}

.sidebar-header h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
}

.sidebar-nav {
    flex: 1;
    padding: 20px 0;
}

.sidebar-nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar-nav li {
    padding: 12px 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: all 0.2s;
}

.sidebar-nav li:hover {
    background-color: #34495e;
}

.sidebar-nav li.active {
    background-color: #3498db;
}

.sidebar-nav li i {
    margin-right: 12px;
    width: 20px;
    text-align: center;
}

.sidebar-footer {
    padding: 20px;
    border-top: 1px solid #3c546c;
}

.logout-btn {
    width: 100%;
    padding: 10px;
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}

.logout-btn:hover {
    background-color: #c0392b;
}

.logout-btn i {
    margin-right: 8px;
}

/* Основной контент */
.content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
}

.content-header {
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.search-bar {
    position: relative;
    width: 300px;
}

.search-bar i {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #999;
}

.search-bar input {
    width: 100%;
    padding: 10px 10px 10px 35px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.user-menu {
    display: flex;
    align-items: center;
}

.user-name {
    margin-right: 10px;
    font-weight: 500;
}

.user-avatar {
    width: 40px;
    height: 40px;
    background-color: #3498db;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.content-body {
    padding: 30px;
    flex: 1;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.page-header h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
}

.add-btn {
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: background-color 0.3s;
}

.add-btn:hover {
    background-color: #219653;
}

.add-btn i {
    margin-right: 8px;
}

/* Таблица товаров */
.items-table-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.items-table {
    width: 100%;
    border-collapse: collapse;
}

.items-table th,
.items-table td {
    padding: 15px;
    text-align: left;
}

.items-table th {
    background-color: #f9fafb;
    font-weight: 600;
    color: #4a5568;
    border-bottom: 1px solid #edf2f7;
}

.items-table tbody tr {
    border-bottom: 1px solid #edf2f7;
}

.items-table tbody tr:hover {
    background-color: #f9fafb;
}

.actions {
    display: flex;
    gap: 8px;
}

.edit-btn,
.delete-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 5px;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.edit-btn {
    color: #3498db;
}

.delete-btn {
    color: #e74c3c;
}

.edit-btn:hover,
.delete-btn:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.loading,
.no-items {
    padding: 40px;
    text-align: center;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    color: #666;
}

.loading i,
.no-items i {
    font-size: 24px;
    margin-bottom: 10px;
    display: block;
}

/* Форма добавления */
.add-form-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
    overflow: hidden;
}

.add-form {
    padding: 20px;
}

.add-form h3 {
    margin-top: 0;
    margin-bottom: 20px;
    color: #333;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #4a5568;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.form-group textarea {
    min-height: 100px;
    resize: vertical;
}

.form-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    margin-top: 20px;
}

.cancel-btn,
.submit-btn {
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}

.cancel-btn {
    background-color: #edf2f7;
    color: #4a5568;
    border: none;
}

.submit-btn {
    background-color: #3498db;
    color: white;
    border: none;
    display: flex;
    align-items: center;
}

.submit-btn i {
    margin-right: 8px;
}

.cancel-btn:hover {
    background-color: #e2e8f0;
}

.submit-btn:hover {
    background-color: #2980b9;
}

/* Модальное окно */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    width: 400px;
    max-width: 90%;
}

.modal h3 {
    margin-top: 0;
    color: #333;
}

.modal-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    margin-top: 20px;
}

.confirm-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.confirm-btn:hover {
    background-color: #c0392b;
}

/* Адаптивность */
@media (max-width: 768px) {
    .admin-layout {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        order: 2;
    }

    .content {
        order: 1;
    }

    .content-header {
        flex-direction: column;
        gap: 15px;
    }

    .search-bar {
        width: 100%;
    }

    .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
}
</style>
