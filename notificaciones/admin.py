from django.contrib import admin
from .models import Notificaciones

@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = ('notificacion_id', 'usuario', 'mensaje', 'leida', 'fecha_envio', 'tipo_canal_notificacion', 'estado_notificacion')
    search_fields = ('usuario__email', 'mensaje',)
    list_filter = ('leida', 'tipo_canal_notificacion', 'estado_notificacion',)