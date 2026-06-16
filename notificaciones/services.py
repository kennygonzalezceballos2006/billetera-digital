from django.utils import timezone
from core.models import Catalogos
from .models import Notificaciones

def crear_notificacion(usuario, mensaje, transaccion=None):
    canal = Catalogos.objects.get(
        catalogo_nombre='push',
        categoria__categoria_nombre='tipo_canal_notificacion'
    )
    estado = Catalogos.objects.get(
        catalogo_nombre='enviada',
        categoria__categoria_nombre='estado_notificacion'
    )
    return Notificaciones.objects.create(
        usuario=usuario,
        mensaje=mensaje,
        fecha_envio=timezone.now(),
        leida=0,
        transaccion=transaccion,
        tipo_canal_notificacion=canal,
        estado_notificacion=estado
    )

def get_notificaciones(usuario_id):
    return Notificaciones.objects.filter(
        usuario_id=usuario_id
    ).order_by('-fecha_envio')[:10]

def marcar_leida(notificacion_id, usuario_id):
    Notificaciones.objects.filter(
        notificacion_id=notificacion_id,
        usuario_id=usuario_id
    ).update(leida=1)

def contar_no_leidas(usuario_id):
    return Notificaciones.objects.filter(
        usuario_id=usuario_id,
        leida=0
    ).count()