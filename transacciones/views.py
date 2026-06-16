from django.shortcuts import render, redirect
from django.contrib import messages
from cuentas.models import Cuentas, Bolsillos
from usuarios.models import Usuarios
from . import services

def transferir_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']
    cuenta = Cuentas.objects.get(usuario_id=usuario_id)

    if request.method == 'POST':
        numero_destino = request.POST.get('numero_destino')
        monto = float(request.POST.get('monto'))
        usuario = Usuarios.objects.get(usuario_id=usuario_id)

        try:
            cuenta_destino = Cuentas.objects.get(numero_cuenta=numero_destino)
            services.transferir(cuenta, cuenta_destino, monto, 'transferencia', usuario)
            messages.success(request, '¡Transferencia exitosa!')
            return redirect('dashboard')
        except Cuentas.DoesNotExist:
            messages.error(request, 'Cuenta destino no encontrada.')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'transferir/transferir.html', {'cuenta': cuenta})

def historial_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']
    cuenta = Cuentas.objects.get(usuario_id=usuario_id)
    historial = services.get_historial(cuenta)

    return render(request, 'historial/historial.html', {
        'historial': historial,
        'cuenta': cuenta
    })