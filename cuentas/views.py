from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from . import services
from decimal import Decimal, InvalidOperation
# Importamos los modelos necesarios
from transacciones.models import Transacciones 
from django.db import transaction
from notificaciones.models import Notificaciones 
from usuarios.models import Usuarios

from .models import Bolsillos
from transacciones import services as trans_services

def dashboard_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        usuario = Usuarios.objects.get(usuario_id=usuario_id)
        cuenta = services.get_cuenta_usuario(usuario_id)
    except Usuarios.DoesNotExist:
        return redirect('login')

    if not cuenta:
        messages.error(request, 'No tienes una cuenta activa.')
        return redirect('login')
    
    persona = usuario.personas_set.first()
    nombre_mostrar = persona.nombres if persona else "Usuario"

    bolsillos = services.get_bolsillos(cuenta)
    saldo_total = services.get_saldo_total(cuenta)

    historial = Transacciones.objects.filter(
        Q(cuenta_origen=cuenta) | Q(cuenta_destino=cuenta)
    ).order_by('-fecha_hora')[:5]

    ahora = timezone.now()
    inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Convertimos los resultados de Sum (que pueden ser Decimales) explícitamente
    gastos_mes = Transacciones.objects.filter(
        cuenta_origen=cuenta,
        fecha_hora__gte=inicio_mes
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    ahorro_mes = Transacciones.objects.filter(
        cuenta_destino=cuenta,
        fecha_hora__gte=inicio_mes
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    total_ingresos = gastos_mes + ahorro_mes
    
    # Cálculos para el gráfico SVG usando Decimal para todo
    circunferencia = Decimal('439.8')
    ciento = Decimal('100')

    if total_ingresos > 0:
        porcentaje_gastos = (gastos_mes / total_ingresos) * ciento
        porcentaje_ahorro = (ahorro_mes / total_ingresos) * ciento
        # Los cálculos de dasharray ahora son todos Decimal
        dasharray_gastos = (porcentaje_gastos / ciento) * circunferencia
        dasharray_ahorro = (porcentaje_ahorro / ciento) * circunferencia
        dashoffset_ahorro = -dasharray_gastos
    else:
        porcentaje_gastos = Decimal('0')
        porcentaje_ahorro = Decimal('0')
        dasharray_gastos = Decimal('0')
        dasharray_ahorro = Decimal('0')
        dashoffset_ahorro = Decimal('0')

    context = {
        'nombre_usuario': nombre_mostrar,
        'email': request.session.get('email'),
        'cuenta': cuenta,
        'bolsillos': bolsillos,
        'saldo_total': saldo_total,
        'historial': historial,
        'no_leidas': Notificaciones.objects.filter(usuario=usuario, leida=False).count(),
        'gastos_mes': gastos_mes,
        'ahorro_mes': ahorro_mes,
        'total_ingresos': total_ingresos,
        'porcentaje_gastos': porcentaje_gastos,
        'porcentaje_ahorro': porcentaje_ahorro,
        'dasharray_gastos': dasharray_gastos,
        'dasharray_ahorro': dasharray_ahorro,
        'dashoffset_ahorro': dashoffset_ahorro,
    }
    return render(request, 'dashboard/dashboard_usuario.html', context)

def bolsillos_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        usuario = Usuarios.objects.get(usuario_id=usuario_id)
        cuenta = services.get_cuenta_usuario(usuario_id)
    except Usuarios.DoesNotExist:
        return redirect('login')

    if not cuenta:
        messages.error(request, 'No tienes una cuenta activa.')
        return redirect('login')

    persona = usuario.personas_set.first()
    nombre_mostrar = persona.nombres if persona else "Usuario"
    bolsillos = services.get_bolsillos(cuenta)

    context = {
        'nombre_usuario': nombre_mostrar,
        'email': request.session.get('email'),
        'cuenta': cuenta,
        'bolsillos': bolsillos,
        'saldo_total': services.get_saldo_total(cuenta),
        'no_leidas': Notificaciones.objects.filter(usuario=usuario, leida=False).count(),
    }
    return render(request, 'bolsillos/bolsillos.html', context)

def cuentas_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        usuario = Usuarios.objects.get(usuario_id=usuario_id)
        cuenta = services.get_cuenta_usuario(usuario_id)
    except Usuarios.DoesNotExist:
        return redirect('login')

    persona = usuario.personas_set.first()
    nombre_mostrar = persona.nombres if persona else "Usuario"

    context = {
        'nombre_usuario': nombre_mostrar,
        'email': request.session.get('email'),
        'cuenta': cuenta,
        'saldo_total': services.get_saldo_total(cuenta),
        'no_leidas': Notificaciones.objects.filter(usuario=usuario, leida=False).count(),
    }
    return render(request, 'cuentas/cuentas.html', context)

# views.py
def crear_bolsillo_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            monto = Decimal(request.POST.get('monto') or 0)
        except (InvalidOperation, ValueError):
            messages.error(request, "Monto inválido.")
            return redirect('cuentas:bolsillos')
            
        usuario_id = request.session['usuario_id']
        cuenta = services.get_cuenta_usuario(usuario_id)

        try:
            # transaction.atomic garantiza que o se crea todo o no se crea nada
            with transaction.atomic():
                # 1. Crear el bolsillo
                services.crear_bolsillo(cuenta, nombre)
                
                # 2. Si hay monto, transferir
                if monto > 0:
                    bolsillo = cuenta.bolsillos_set.order_by('-bolsillo_id').first()
                    
                    # Llamamos al servicio que debe manejar la lógica financiera
                    trans_services.transferir_a_bolsillo(cuenta, bolsillo, monto)
            
            messages.success(request, f'Bolsillo "{nombre}" creado exitosamente.')
        except Exception as e:
            # Esto captura cualquier error de saldo insuficiente o base de datos
            messages.error(request, f'Error: {str(e)}')

    return redirect('cuentas:bolsillos')
# views.py
def eliminar_bolsillo_view(request, bolsillo_id):
    if not request.session.get('usuario_id'):
        return redirect('login')

    if request.method == 'POST':
        try:
            bolsillo = Bolsillos.objects.get(
                bolsillo_id=bolsillo_id,
                cuenta__usuario_id=request.session['usuario_id']
            )

            # 1. NUEVA VALIDACIÓN: Obligar a retirar el dinero
            if bolsillo.saldo > 0:
                messages.error(request, 'El bolsillo aún tiene fondos. Debes retirar el dinero antes de eliminarlo.')
                return redirect('cuentas:bolsillos')

            # 2. VERIFICACIÓN DE INTEGRIDAD (Historial de transacciones)
            if bolsillo.transacciones_set.exists():
                messages.error(request, 'No puedes eliminar este bolsillo porque tiene un historial de transacciones.')
                return redirect('cuentas:bolsillos')

            # 3. ELIMINACIÓN
            # Como ya validamos que el saldo es 0, no hace falta modificar el saldo de la cuenta
            bolsillo.delete()
            messages.success(request, 'Bolsillo eliminado correctamente.')

        except Bolsillos.DoesNotExist:
            messages.error(request, 'Bolsillo no encontrado.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el bolsillo: {str(e)}')

    return redirect('cuentas:bolsillos')


def procesar_dinero_bolsillo(request):
    if request.method != 'POST':
        return redirect('cuentas:bolsillos')

    bolsillo_id = request.POST.get('bolsillo_id')
    accion = request.POST.get('accion')
    
    try:
        monto = Decimal(request.POST.get('monto') or 0)
        # VALIDACIÓN DE SEGURIDAD: Evitar montos menores o iguales a cero
        if monto <= 0:
            messages.error(request, 'El monto debe ser mayor a cero.')
            return redirect('cuentas:bolsillos')
    except (InvalidOperation, ValueError):
        messages.error(request, 'Monto inválido.')
        return redirect('cuentas:bolsillos')
    
    try:
        # Usamos transaction.atomic para garantizar la integridad financiera
        with transaction.atomic():
            bolsillo = Bolsillos.objects.select_for_update().get(
                bolsillo_id=bolsillo_id, 
                cuenta__usuario_id=request.session['usuario_id']
            )
            cuenta = bolsillo.cuenta
            
            if accion == 'agregar':
                if cuenta.saldo_disponible >= monto:
                    cuenta.saldo_disponible -= monto
                    bolsillo.saldo += monto
                    cuenta.saldo_bolsillos += monto 
                    cuenta.save()
                    bolsillo.save()
                    messages.success(request, 'Dinero agregado al bolsillo.')
                else:
                    messages.error(request, 'No tienes suficiente saldo disponible.')
            
            elif accion == 'retirar':
                if bolsillo.saldo >= monto:
                    bolsillo.saldo -= monto
                    cuenta.saldo_disponible += monto
                    cuenta.saldo_bolsillos -= monto 
                    cuenta.save()
                    bolsillo.save()
                    messages.success(request, 'Dinero retirado correctamente.')
                else:
                    messages.error(request, 'El bolsillo no tiene fondos suficientes.')
            else:
                messages.error(request, 'Acción no reconocida.')
                    
    except Bolsillos.DoesNotExist:
        messages.error(request, 'Bolsillo no encontrado.')
    except Exception as e:
        messages.error(request, f'Error inesperado: {str(e)}')
            
    return redirect('cuentas:bolsillos')

def historial_view(request):
    # Esto es temporal para que el servidor arranque. 
    # Luego aquí pondrás la lógica de tu historial.
    return render(request, 'historial.html', {})