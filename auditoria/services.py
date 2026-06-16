from django.utils import timezone
from .models import Auditoriasistema

def registrar(accion, tabla_afectada, ip, id_registro=None,
              valor_anterior=None, valor_nuevo=None,
              usuario_id=None, dispositivo_id=None):
    Auditoriasistema.objects.create(
        accion=accion,
        tabla_afectada=tabla_afectada,
        id_registro=id_registro,
        valor_anterior=valor_anterior,
        valor_nuevo=valor_nuevo,
        fecha=timezone.now(),
        ip=ip,
        dispositivo=dispositivo_id,
        usuario_id=usuario_id
    )