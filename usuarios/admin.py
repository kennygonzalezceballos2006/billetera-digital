from django.contrib import admin
from .models import Usuarios, Personas, Comercios, Empresas

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'email', 'fecha_registro', 'rol', 'estado_cliente', 'tipo_cliente')
    search_fields = ('email',)
    list_filter = ('rol', 'estado_cliente', 'tipo_cliente')

@admin.register(Personas)
class PersonasAdmin(admin.ModelAdmin):
    list_display = ('persona_id', 'nombres', 'apellidos', 'identificacion', 'telefono', 'usuario')
    search_fields = ('nombres', 'apellidos', 'identificacion',)

@admin.register(Comercios)
class ComerciosAdmin(admin.ModelAdmin):
    list_display = ('comercio_id', 'nombre_establecimiento', 'direccion', 'telefono_comercio', 'persona')
    search_fields = ('nombre_establecimiento',)

@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('empresa_id', 'nit', 'razon_social', 'direccion', 'persona')
    search_fields = ('razon_social', 'nit',)
