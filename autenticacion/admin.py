from django.contrib import admin
from .models import Dispositivos, Sesiones, Codigosotp

@admin.register(Dispositivos)
class DispositivosAdmin(admin.ModelAdmin):
    list_display = ('dispositivo_id', 'fingerprint', 'sistema_operativo', 'activo', 'usuario')
    search_fields = ('fingerprint',)
    list_filter = ('activo',)

@admin.register(Sesiones)
class SesionesAdmin(admin.ModelAdmin):
    list_display = ('sesion_id', 'usuario', 'fecha_inicio', 'fecha_expiracion', 'ip')
    search_fields = ('usuario__email',)

@admin.register(Codigosotp)
class CodigosotpAdmin(admin.ModelAdmin):
    list_display = ('otp_id', 'usuario', 'codigo', 'estado_otp', 'intentos', 'fecha_creacion')
    search_fields = ('usuario__email',)
    list_filter = ('estado_otp',)