from django.shortcuts import render, redirect
from django.contrib import messages
from . import services

def dashboard_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']
    cuenta = services.get_cuenta_usuario(usuario_id)

    if not cuenta:
        messages.error(request, 'No tienes una cuenta activa.')
        return redirect('login')

    bolsillos = services.get_bolsillos(cuenta)
    saldo_total = services.get_saldo_total(cuenta)

    context = {
        'cuenta': cuenta,
        'bolsillos': bolsillos,
        'saldo_total': saldo_total,
        'email': request.session.get('email'),
    }
    return render(request, 'dashboard/dashboard.html', context)