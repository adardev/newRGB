from django.contrib import admin
from django.urls import path
from bluetoothcontrol.views import mover_angulo, secuencia, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('mover_angulo/', mover_angulo, name='mover_angulo'),
    path('secuencia/', secuencia, name='secuencia')
]