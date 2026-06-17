from django.shortcuts import render, redirect
from django.contrib import messages
from . import services

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        usuario, error = services.autenticar_usuario(email, password)

        if error:
            messages.error(request, error)
            return render(request, 'login/login.html')

        # Guardar en sesión Django
        request.session['usuario_id'] = usuario.usuario_id
        request.session['email'] = usuario.email
        request.session['tipo_cliente'] = usuario.tipo_cliente.catalogo_nombre

        return redirect('cuentas:dashboard')

    return render(request, 'login/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')