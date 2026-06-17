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

    # --- LÓGICA DE RESUMEN DEL MES (DINÁMICA) ---
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