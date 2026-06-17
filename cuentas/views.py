from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from . import services

# Importamos los modelos necesarios
from transacciones.models import Transacciones 
from notificaciones.models import Notificaciones 
from usuarios.models import Usuarios

def dashboard_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    # Obtenemos el usuario y la cuenta
    try:
        usuario = Usuarios.objects.get(usuario_id=usuario_id)
        cuenta = services.get_cuenta_usuario(usuario_id)
    except Usuarios.DoesNotExist:
        return redirect('login')

    if not cuenta:
        messages.error(request, 'No tienes una cuenta activa.')
        return redirect('login')
    
    # Obtener el nombre desde la tabla Personas
    persona = usuario.personas_set.first()
    nombre_mostrar = persona.nombres if persona else "Usuario"

    # Datos básicos
    bolsillos = services.get_bolsillos(cuenta)
    saldo_total = services.get_saldo_total(cuenta)

    # Historial reciente
    historial = Transacciones.objects.filter(
        Q(cuenta_origen=cuenta) | Q(cuenta_destino=cuenta)
    ).order_by('-fecha_hora')[:5]

    # logica de resumen del mes
    ahora = timezone.now()
    inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculamos gastos (ejemplo: transacciones donde la cuenta es origen)
    gastos_mes = Transacciones.objects.filter(
        cuenta_origen=cuenta,
        fecha_hora__gte=inicio_mes
    ).aggregate(total=Sum('monto'))['total'] or 0

    # Calculamos ahorros (ejemplo: transferencias hacia bolsillos)
    ahorro_mes = Transacciones.objects.filter(
        cuenta_destino=cuenta,
        fecha_hora__gte=inicio_mes
    ).aggregate(total=Sum('monto'))['total'] or 0

    total_ingresos = gastos_mes + ahorro_mes
    
    # Cálculos para el gráfico SVG
    # La circunferencia de un círculo con r=70 es aprox 439.8
    circunferencia = 439.8
    if total_ingresos > 0:
        porcentaje_gastos = (gastos_mes / total_ingresos) * 100
        porcentaje_ahorro = (ahorro_mes / total_ingresos) * 100
        dasharray_gastos = (porcentaje_gastos / 100) * circunferencia
        dasharray_ahorro = (porcentaje_ahorro / 100) * circunferencia
        dashoffset_ahorro = -dasharray_gastos
    else:
        porcentaje_gastos = 0
        porcentaje_ahorro = 0
        dasharray_gastos = 0
        dasharray_ahorro = 0
        dashoffset_ahorro = 0

    context = {
        'nombre_usuario': nombre_mostrar,
        'email': request.session.get('email'),
        'cuenta': cuenta,
        'bolsillos': bolsillos,
        'saldo_total': saldo_total,
        'historial': historial,
        'no_leidas': Notificaciones.objects.filter(usuario=usuario, leida=False).count(),
        
        # Variables para el Resumen del Mes
        'gastos_mes': gastos_mes,
        'ahorro_mes': ahorro_mes,
        'total_ingresos': total_ingresos,
        'porcentaje_gastos': porcentaje_gastos,
        'porcentaje_ahorro': porcentaje_ahorro,
        'dasharray_gastos': dasharray_gastos,
        'dasharray_ahorro': dasharray_ahorro,
        'dashoffset_ahorro': dashoffset_ahorro,
    }
    print("Datos enviados al template:", context['total_ingresos'])
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
        monto = request.POST.get('monto') or 0
        usuario_id = request.session['usuario_id']
        cuenta = services.get_cuenta_usuario(usuario_id)

        try:
            services.crear_bolsillo(cuenta, nombre)
            # Si tiene monto inicial, descontar del saldo disponible
            if float(monto) > 0:
                from transacciones import services as trans_services
                bolsillo = cuenta.bolsillos_set.order_by('-bolsillo_id').first()
                trans_services.transferir_a_bolsillo(cuenta, bolsillo, float(monto))
            messages.success(request, f'Bolsillo "{nombre}" creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return redirect('bolsillos')

# views.py
def eliminar_bolsillo_view(request, bolsillo_id):
    if not request.session.get('usuario_id'):
        return redirect('login')
    if request.method == 'POST':
        from .models import Bolsillos
        try:
            bolsillo = Bolsillos.objects.get(
                bolsillo_id=bolsillo_id,
                cuenta__usuario_id=request.session['usuario_id']
            )
            # Devolver saldo al disponible
            if bolsillo.saldo > 0:
                bolsillo.cuenta.saldo_disponible += bolsillo.saldo
                bolsillo.cuenta.saldo_bolsillos -= bolsillo.saldo
                bolsillo.cuenta.save()
            bolsillo.delete()
            messages.success(request, 'Bolsillo eliminado.')
        except Bolsillos.DoesNotExist:
            messages.error(request, 'Bolsillo no encontrado.')
    return redirect('bolsillos')
