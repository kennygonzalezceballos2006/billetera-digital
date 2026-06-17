from django.utils import timezone
from core.models import Catalogos
from .models import Cuentas, Bolsillos
import random

def get_cuenta_usuario(usuario_id):
    try:
        return Cuentas.objects.get(usuario_id=usuario_id)
    except Cuentas.DoesNotExist:
        return None

def get_bolsillos(cuenta):
    return Bolsillos.objects.filter(cuenta=cuenta)

def get_saldo_total(cuenta):
    return cuenta.saldo_disponible + cuenta.saldo_bolsillos

def crear_cuenta(usuario):
    estado_activa = Catalogos.objects.get(
        catalogo_nombre='ACTIVA',
        categoria__categoria_nombre='estado_cuenta'
    )
    numero_cuenta = str(random.randint(1000000000, 9999999999))
    return Cuentas.objects.create(
        usuario=usuario,
        saldo_disponible=0.0000,
        saldo_bolsillos=0.0000,
        numero_cuenta=numero_cuenta,
        fecha_creacion=timezone.now(),
        movimientos_mes_actual=0.0000,
        estado_cuenta=estado_activa
    )

def crear_bolsillo(cuenta, nombre):
    return Bolsillos.objects.create(
        nombre=nombre,
        saldo=0.0000,
        fecha_creacion=timezone.now(),
        fecha_modificacion=timezone.now(),
        cuenta=cuenta
    )

def agregar_a_bolsillo(cuenta, bolsillo, monto):
    monto = float(monto)

    if monto <= 0:
        raise ValueError('El monto debe ser mayor a 0.')

    if cuenta.saldo_disponible < monto:
        raise ValueError('Saldo disponible insuficiente.')

    cuenta.saldo_disponible -= monto
    cuenta.saldo_bolsillos += monto
    cuenta.save()

    bolsillo.saldo += monto
    bolsillo.fecha_modificacion = timezone.now()
    bolsillo.save()

    return bolsillo

def retirar_de_bolsillo(cuenta, bolsillo, monto):
    monto = float(monto)

    if monto <= 0:
        raise ValueError('El monto debe ser mayor a 0.')

    if bolsillo.saldo < monto:
        raise ValueError('El bolsillo no tiene saldo suficiente.')

    bolsillo.saldo -= monto
    bolsillo.fecha_modificacion = timezone.now()
    bolsillo.save()

    cuenta.saldo_disponible += monto
    cuenta.saldo_bolsillos -= monto
    cuenta.save()

    return bolsillo

def eliminar_bolsillo(bolsillo_id, usuario_id):
    bolsillo = Bolsillos.objects.get(
        bolsillo_id=bolsillo_id,
        cuenta__usuario_id=usuario_id
    )
    if bolsillo.saldo > 0:
        bolsillo.cuenta.saldo_disponible += bolsillo.saldo
        bolsillo.cuenta.saldo_bolsillos -= bolsillo.saldo
        bolsillo.cuenta.save()
    bolsillo.delete()