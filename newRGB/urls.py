from django.contrib import admin
from django.urls import path
from bluetoothcontrol.views import enviar_rgb, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('enviar_rgb/', enviar_rgb, name='enviar_rgb'),
]