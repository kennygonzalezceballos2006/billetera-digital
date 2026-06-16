from django.contrib import admin
from .models import Auditoriasistema

@admin.register(Auditoriasistema)
class AuditoriasistemaAdmin(admin.ModelAdmin):
    list_display = ('auditoria_id', 'accion', 'tabla_afectada', 'id_registro', 'usuario_id', 'fecha', 'ip')
    search_fields = ('accion', 'tabla_afectada',)
    list_filter = ('accion', 'tabla_afectada',)