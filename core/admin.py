from django.contrib import admin
from .models import Categorias, Catalogos
# Register your models here.

@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('categoria_id', 'categoria_nombre')
    search_fields = ('categoria_nombre',)

@admin.register(Catalogos)
class CatalogosAdmin(admin.ModelAdmin):
    list_display = ('catalogo_id', 'catalogo_nombre', 'categoria')
    search_fields = ('catalogo_nombre',)
    list_filter = ('categoria',)