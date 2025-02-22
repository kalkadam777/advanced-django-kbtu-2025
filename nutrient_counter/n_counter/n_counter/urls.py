
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('delete/<int:id>/', views.delete_consume, name="delete"),
    path('chart-data/', views.nutrient_data, name="chart-data"),
    path("register/", views.register, name="register"),
    path("add-food/", views.add_food, name="add-food"),
    path("update-goals/", views.update_goals, name="update-goals"),
]

urlpatterns += [
    path("login/", auth_views.LoginView.as_view(template_name="app/login.html"), name="login"),
    path("logout/", views.custom_logout, name="logout"),
]
