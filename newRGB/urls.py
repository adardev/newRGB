from django.contrib import admin
from django.urls import path
from bluetoothcontrol.views import recibir_datos  # ✅ Importar directamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sensores/', recibir_datos),  # ✅ Usar directamente la función
]