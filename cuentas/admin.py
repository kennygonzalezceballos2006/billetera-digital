from django.contrib import admin
from .models import Cuentas, Bolsillos

@admin.register(Cuentas)
class CuentasAdmin(admin.ModelAdmin):
    list_display = ('cuenta_id', 'numero_cuenta', 'saldo_disponible', 'saldo_bolsillos', 'usuario', 'estado_cuenta')
    search_fields = ('numero_cuenta', 'usuario__email',)
    list_filter = ('estado_cuenta',)

@admin.register(Bolsillos)
class BolsillosAdmin(admin.ModelAdmin):
    list_display = ('bolsillo_id', 'nombre', 'saldo', 'cuenta', 'fecha_modificacion')
    search_fields = ('nombre',)