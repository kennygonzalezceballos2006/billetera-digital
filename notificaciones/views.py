from django.shortcuts import render, redirect
from . import services

def notificaciones_view(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session['usuario_id']
    notificaciones = services.get_notificaciones(usuario_id)

    return render(request, 'notificaciones/notificaciones.html', {
        'notificaciones': notificaciones,
        'no_leidas': services.contar_no_leidas(usuario_id)
    })

def marcar_leida_view(request, notificacion_id):
    if not request.session.get('usuario_id'):
        return redirect('login')

    services.marcar_leida(notificacion_id, request.session['usuario_id'])
    return redirect('notificaciones')