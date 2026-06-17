from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import uuid
from cuentas.models import Cuentas
from transacciones.models import Transacciones
from . import services

def transferir_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        # Obtenemos la cuenta única del usuario
        cuenta = Cuentas.objects.get(usuario_id=usuario_id)
        historial = services.get_historial(cuenta)
    except Cuentas.DoesNotExist:
        messages.error(request, "No tienes una cuenta asociada.")
        return redirect('dashboard')

    return render(request, 'transferir/transferencia_general.html', {
        'cuenta': cuenta,
        'historial': historial
    })

def procesar_transferencia_view(request):
    if request.method != 'POST':
        return redirect('transferir')

    usuario_id = request.session.get('usuario_id')
    # Ajusta 'numero_cuenta' si en tu modelo Cuentas se llama diferente
    num_destino = request.POST.get('destinatario')
    
    try:
        monto = Decimal(request.POST.get('monto') or 0)
        if monto <= 0:
            messages.error(request, 'El monto debe ser mayor a cero.')
            return redirect('transferir')
    except (InvalidOperation, ValueError):
        messages.error(request, 'Monto inválido.')
        return redirect('transferir')

    try:
        with transaction.atomic():
            # 1. Bloqueamos cuenta origen y buscamos destino
            cuenta_origen = Cuentas.objects.select_for_update().get(usuario_id=usuario_id)
            cuenta_destino = Cuentas.objects.get(numero_cuenta=num_destino)
            
            if cuenta_origen.cuenta_id == cuenta_destino.cuenta_id:
                messages.error(request, "No puedes transferir dinero a tu propia cuenta.")
                return redirect('transferir')
            
            # 2. Verificación de fondos
            if cuenta_origen.saldo_disponible >= monto:
                cuenta_origen.saldo_disponible -= monto
                cuenta_origen.save()
                
                cuenta_destino.saldo_disponible += monto
                cuenta_destino.save()
                
                # 3. Crear registro cumpliendo el CHK_DESTINO
                Transacciones.objects.create(
                    idempotency_key=str(uuid.uuid4()),
                    monto=monto,
                    monto_total=monto,
                    gmf_cobrado=0,
                    fecha_hora=timezone.now(),
                    cuenta_origen=cuenta_origen,
                    cuenta_destino=cuenta_destino,  # <--- Satisface chk_destino
                    bolsillo_destino=None,          # <--- Satisface chk_destino
                    tipo_transaccion_id=27,      
                    estado_transaccion_id=21     
                )
                
                messages.success(request, f'Transferencia de ${monto} exitosa.')
            else:
                messages.error(request, 'Saldo insuficiente.')
                
    except Cuentas.DoesNotExist:
        messages.error(request, 'La cuenta destino no existe.')
    except Exception as e:
        messages.error(request, f'Error al procesar: {str(e)}')
            
    return redirect('transferir')

def dashboard_view(request):
    return render(request, 'dashboard.html')