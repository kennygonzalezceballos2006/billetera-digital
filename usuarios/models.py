# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from core.models import Catalogos

class Usuarios(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=254)
    password_hash = models.CharField(max_length=60)
    fecha_registro = models.DateTimeField()
    rol = models.ForeignKey(Catalogos, models.DO_NOTHING)
    estado_cliente = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='usuarios_estado_cliente_set')
    tipo_cliente = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='usuarios_tipo_cliente_set')
    
    class Meta:
        managed = False
        db_table = 'Usuarios'


class Personas(models.Model):
    persona_id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    identificacion = models.CharField(unique=True, max_length=20)
    fecha_nacimiento = models.DateTimeField()
    fecha_expedicion_documento = models.DateTimeField()
    pais_nacimiento = models.ForeignKey(Catalogos, models.DO_NOTHING)
    municipio_nacimiento = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='personas_municipio_nacimiento_set')
    lugar_expedicion_documento = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='personas_lugar_expedicion_documento_set')
    sexo = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='personas_sexo_set')
    tipo_documento = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='personas_tipo_documento_set')
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Personas'

class Comercios(models.Model):
    comercio_id = models.AutoField(primary_key=True)
    nombre_establecimiento = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    telefono_comercio = models.CharField(max_length=20)
    tipo_comercio = models.ForeignKey(Catalogos, models.DO_NOTHING)
    persona = models.ForeignKey(Personas, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Comercios'

class Empresas(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nit = models.CharField(unique=True, max_length=20)
    razon_social = models.CharField(max_length=150)
    codigo_ciiu = models.CharField(max_length=10)
    fecha_constitucion = models.DateTimeField()
    direccion = models.CharField(max_length=150)
    telefono_empresa = models.CharField(max_length=20)
    tipo_empresa = models.ForeignKey(Catalogos, models.DO_NOTHING)
    persona = models.ForeignKey(Personas, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Empresas'