from django.contrib import admin
from .models import Transacciones, Limitetransacciones

@admin.register(Transacciones)
class TransaccionesAdmin(admin.ModelAdmin):
    list_display = ('transaccion_id', 'monto', 'gmf_cobrado', 'monto_total', 'tipo_transaccion', 'estado_transaccion', 'fecha_hora')
    search_fields = ('idempotency_key',)
    list_filter = ('tipo_transaccion', 'estado_transaccion',)

@admin.register(Limitetransacciones)
class LimitetransaccionesAdmin(admin.ModelAdmin):
    list_display = ('limite_id', 'tipo_usuario', 'tipo_transaccion', 'tope_mensual_sin_gmf', 'gmf_porcentaje')
    list_filter = ('tipo_usuario', 'tipo_transaccion',)