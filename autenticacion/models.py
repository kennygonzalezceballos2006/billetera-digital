from django.db import models
from core.models import Catalogos
from usuarios.models import Usuarios

class Dispositivos(models.Model):
    dispositivo_id = models.AutoField(primary_key=True)
    fingerprint = models.CharField(unique=True, max_length=64)
    sistema_operativo = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField()
    activo = models.IntegerField()
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'Dispositivos'

class Sesiones(models.Model):
    sesion_id = models.AutoField(primary_key=True)
    token_hash = models.CharField(unique=True, max_length=64)
    fecha_inicio = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    ip = models.CharField(max_length=45)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    dispositivo = models.ForeignKey(Dispositivos, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'Sesiones'

class Codigosotp(models.Model):
    otp_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=6)
    fecha_creacion = models.DateTimeField()
    estado_otp = models.IntegerField()
    intentos = models.IntegerField()
    tipo_otp = models.ForeignKey(Catalogos, models.DO_NOTHING)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'CodigosOTP'