# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categorias(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    categoria_nombre = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'Categorias'


class Catalogos(models.Model):
    catalogo_id = models.AutoField(primary_key=True)
    catalogo_nombre = models.CharField(unique=True, max_length=100)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Catalogos'
        unique_together = (('categoria', 'catalogo_nombre'),)
