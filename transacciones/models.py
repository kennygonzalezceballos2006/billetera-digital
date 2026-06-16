from django.db import models
from core.models import Catalogos
from cuentas.models import Cuentas, Bolsillos

class Transacciones(models.Model):
    transaccion_id = models.AutoField(primary_key=True)
    idempotency_key = models.CharField(unique=True, max_length=64)
    monto = models.DecimalField(max_digits=15, decimal_places=4)
    gmf_cobrado = models.DecimalField(max_digits=15, decimal_places=4)
    monto_total = models.DecimalField(max_digits=15, decimal_places=4)
    fecha_hora = models.DateTimeField()
    cuenta_origen = models.ForeignKey(Cuentas, models.DO_NOTHING, blank=True, null=True)
    bolsillo_origen = models.ForeignKey(Bolsillos, models.DO_NOTHING, blank=True, null=True)
    cuenta_destino = models.ForeignKey(Cuentas, models.DO_NOTHING, related_name='transacciones_cuenta_destino_set', blank=True, null=True)
    bolsillo_destino = models.ForeignKey(Bolsillos, models.DO_NOTHING, related_name='transacciones_bolsillo_destino_set', blank=True, null=True)
    tipo_transaccion = models.ForeignKey(Catalogos, models.DO_NOTHING)
    estado_transaccion = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='transacciones_estado_transaccion_set')
    class Meta:
        managed = False
        db_table = 'Transacciones'

class Limitetransacciones(models.Model):
    limite_id = models.AutoField(primary_key=True)
    tope_mensual_sin_gmf = models.DecimalField(max_digits=15, decimal_places=4)
    gmf_porcentaje = models.DecimalField(max_digits=15, decimal_places=4)
    tipo_usuario = models.ForeignKey(Catalogos, models.DO_NOTHING)
    tipo_transaccion = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='limitetransacciones_tipo_transaccion_set')
    class Meta:
        managed = False
        db_table = 'LimiteTransacciones'
        unique_together = (('tipo_usuario', 'tipo_transaccion'),)