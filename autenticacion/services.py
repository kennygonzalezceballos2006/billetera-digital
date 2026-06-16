from django.contrib.auth.hashers import check_password
from django.utils import timezone
from usuarios.models import Usuarios

def autenticar_usuario(email, password):
    try:
        usuario = Usuarios.objects.get(email=email)
    except Usuarios.DoesNotExist:
        return None, 'Email o contraseña incorrectos.'

    if not check_password(password, usuario.password_hash):
        return None, 'Email o contraseña incorrectos.'

    if usuario.estado_cliente.catalogo_nombre != 'Activo':
        return None, 'Tu cuenta está inactiva o bloqueada.'

    return usuario, None