from django.utils import timezone
from django.db import transaction
import uuid
from core.models import Catalogos
from cuentas.models import Cuentas, Bolsillos
from .models import Transacciones, Limitetransacciones

def get_limite(tipo_usuario, tipo_transaccion_nombre):
    try:
        tipo_transaccion = Catalogos.objects.get(
            catalogo_nombre=tipo_transaccion_nombre,
            categoria__categoria_nombre='tipo_transaccion'
        )
        return Limitetransacciones.objects.get(
            tipo_usuario=tipo_usuario,
            tipo_transaccion=tipo_transaccion
        )
    except (Limitetransacciones.DoesNotExist, Catalogos.DoesNotExist):
        return None

def calcular_gmf(monto, limite):
    if limite and limite.tope_mensual_sin_gmf > 0:
        return round(monto * limite.gmf_porcentaje / 100, 4)
    return 0

def aplica_gmf(cuenta, monto, limite):
    if not limite:
        return False
    return (cuenta.movimientos_mes_actual + monto) > limite.tope_mensual_sin_gmf

@transaction.atomic
def transferir(cuenta_origen, cuenta_destino, monto, tipo_transaccion_nombre, usuario):
    limite = get_limite(usuario.tipo_cliente, tipo_transaccion_nombre)

    # Verificar saldo suficiente
    if cuenta_origen.saldo_disponible < monto:
        raise ValueError('Saldo insuficiente.')

    # Calcular GMF
    gmf = calcular_gmf(monto, limite) if aplica_gmf(cuenta_origen, monto, limite) else 0
    monto_total = monto + gmf

    # Verificar saldo suficiente con GMF
    if cuenta_origen.saldo_disponible < monto_total:
        raise ValueError('Saldo insuficiente para cubrir el GMF.')

    tipo_transaccion = Catalogos.objects.get(
        catalogo_nombre=tipo_transaccion_nombre,
        categoria__categoria_nombre='tipo_transaccion'
    )
    estado_exitosa = Catalogos.objects.get(
        catalogo_nombre='exitosa',
        categoria__categoria_nombre='estado_transaccion'
    )

    # Crear transacción
    transaccion = Transacciones.objects.create(
        idempotency_key=str(uuid.uuid4()),
        monto=monto,
        gmf_cobrado=gmf,
        monto_total=monto_total,
        fecha_hora=timezone.now(),
        cuenta_origen=cuenta_origen,
        cuenta_destino=cuenta_destino,
        tipo_transaccion=tipo_transaccion,
        estado_transaccion=estado_exitosa
    )

    # Actualizar saldos
    cuenta_origen.saldo_disponible -= monto_total
    cuenta_origen.movimientos_mes_actual += monto
    cuenta_origen.save()

    cuenta_destino.saldo_disponible += monto
    cuenta_destino.save()

    return transaccion

@transaction.atomic
def transferir_a_bolsillo(cuenta, bolsillo, monto):
    if cuenta.saldo_disponible < monto:
        raise ValueError('Saldo insuficiente.')

    tipo_transaccion = Catalogos.objects.get(
        catalogo_nombre='deposito',
        categoria__categoria_nombre='tipo_transaccion'
    )
    estado_exitosa = Catalogos.objects.get(
        catalogo_nombre='exitosa',
        categoria__categoria_nombre='estado_transaccion'
    )

    transaccion = Transacciones.objects.create(
        idempotency_key=str(uuid.uuid4()),
        monto=monto,
        gmf_cobrado=0,
        monto_total=monto,
        fecha_hora=timezone.now(),
        cuenta_origen=cuenta,
        bolsillo_destino=bolsillo,
        tipo_transaccion=tipo_transaccion,
        estado_transaccion=estado_exitosa
    )

    cuenta.saldo_disponible -= monto
    cuenta.saldo_bolsillos += monto
    cuenta.save()

    bolsillo.saldo += monto
    bolsillo.fecha_modificacion = timezone.now()
    bolsillo.save()

    return transaccion

def get_historial(cuenta):
    return Transacciones.objects.filter(
        cuenta_origen=cuenta
    ).order_by('-fecha_hora')[:10]