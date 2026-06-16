from django.db import models
from core.models import Catalogos
from usuarios.models import Usuarios

class Cuentas(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    saldo_disponible = models.DecimalField(max_digits=15, decimal_places=4)
    saldo_bolsillos = models.DecimalField(max_digits=15, decimal_places=4)
    numero_cuenta = models.CharField(unique=True, max_length=20)
    fecha_creacion = models.DateTimeField()
    movimientos_mes_actual = models.DecimalField(max_digits=15, decimal_places=4)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    estado_cuenta = models.ForeignKey(Catalogos, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'Cuentas'

class Bolsillos(models.Model):
    bolsillo_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=15, decimal_places=4)
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField()
    cuenta = models.ForeignKey(Cuentas, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'Bolsillos'