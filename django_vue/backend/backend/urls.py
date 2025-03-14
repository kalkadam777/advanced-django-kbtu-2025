from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import debug_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('drf-auth/', include('rest_framework.urls', namespace='rest_framework')),
     path("api/debug/", debug_login)
]
