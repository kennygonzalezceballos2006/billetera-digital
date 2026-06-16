from django.db import models
from core.models import Catalogos
from usuarios.models import Usuarios
from transacciones.models import Transacciones

class Notificaciones(models.Model):
    notificacion_id = models.AutoField(primary_key=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField()
    leida = models.IntegerField()
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    transaccion = models.ForeignKey(Transacciones, models.DO_NOTHING, blank=True, null=True)
    tipo_canal_notificacion = models.ForeignKey(Catalogos, models.DO_NOTHING)
    estado_notificacion = models.ForeignKey(Catalogos, models.DO_NOTHING, related_name='notificaciones_estado_notificacion_set')
    class Meta:
        managed = False
        db_table = 'Notificaciones'