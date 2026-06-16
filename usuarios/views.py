# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from . import services

def registro_view(request):
    context = services.get_context_registro()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo_usuario')
        identificacion = request.POST.get('identificacion')

        if services.email_existe(email):
            messages.error(request, 'El email ya está registrado.')
            return render(request, 'registro/registro.html', context)

        if services.identificacion_existe(identificacion):
            messages.error(request, 'La identificación ya está registrada.')
            return render(request, 'registro/registro.html', context)

        try:
            services.registrar(request.POST, tipo, email, password)
            messages.success(request, '¡Registro exitoso!')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'registro/registro.html', context)