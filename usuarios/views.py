# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from core.models import Catalogos
from .models import Usuarios, Personas, Comercios, Empresas

def registro_view(request):
    # Datos para los selects del formulario
    tipos_documento = Catalogos.objects.filter(categoria__categoria_nombre='tipo_documento')
    sexos = Catalogos.objects.filter(categoria__categoria_nombre='sexo')
    municipios = Catalogos.objects.filter(categoria__categoria_nombre='municipio')
    tipos_comercio = Catalogos.objects.filter(categoria__categoria_nombre='tipo_comercio')
    tipos_empresa = Catalogos.objects.filter(categoria__categoria_nombre='tipo_empresa')
    paises = Catalogos.objects.filter(categoria__categoria_nombre='pais')

    context = {
        'tipos_documento': tipos_documento,
        'sexos': sexos,
        'municipios': municipios,
        'tipos_comercio': tipos_comercio,
        'tipos_empresa': tipos_empresa,
        'paises': paises,
    }

    if request.method == 'POST':
        tipo = request.POST.get('tipo_usuario')  # 'persona', 'comercio', 'empresa'
        email = request.POST.get('email')
        password = request.POST.get('password')
        identificacion = request.POST.get('identificacion')

        # Verificar que el email no exista
        if Usuarios.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return render(request, 'registro/registro.html', context)

        # Verificar que la identificación no exista
        if Personas.objects.filter(identificacion=identificacion).exists():
            messages.error(request, 'La identificación ya está registrada.')
            return render(request, 'registro/registro.html', context)

        try:
            # Obtener catálogos necesarios
            tipo_cliente_map = {
                'persona': 'persona',
                'comercio': 'Comercio',
                'empresa': 'Empresa'
            }
            tipo_cliente = Catalogos.objects.get(
                catalogo_nombre=tipo_cliente_map[tipo],
                categoria__categoria_nombre='tipo_usuario'
            )
            estado_activo = Catalogos.objects.get(
                catalogo_nombre='Activo',
                categoria__categoria_nombre='estado_usuario'
            )
            rol_usuario = Catalogos.objects.get(
                catalogo_nombre='Usuario',
                categoria__categoria_nombre='rol'
            )

            # 1. Crear Usuario con argon2
            usuario = Usuarios.objects.create(
                email=email,
                password_hash=make_password(password),
                fecha_registro=timezone.now(),
                rol=rol_usuario,
                estado_cliente=estado_activo,
                tipo_cliente=tipo_cliente
            )

            # 2. Crear Persona (siempre, para los 3 tipos)
            persona = Personas.objects.create(
                nombres=request.POST.get('nombres'),
                apellidos=request.POST.get('apellidos'),
                telefono=request.POST.get('telefono'),
                identificacion=identificacion,
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                fecha_expedicion_documento=request.POST.get('fecha_expedicion_documento'),
                pais_nacimiento_id=request.POST.get('pais_nacimiento'),
                municipio_nacimiento_id=request.POST.get('municipio_nacimiento'),
                lugar_expedicion_documento_id=request.POST.get('lugar_expedicion_documento'),
                sexo_id=request.POST.get('sexo'),
                tipo_documento_id=request.POST.get('tipo_documento'),
                usuario=usuario
            )

            # 3. Según tipo, crear Comercio o Empresa
            if tipo == 'comercio':
                Comercios.objects.create(
                    nombre_establecimiento=request.POST.get('nombre_establecimiento'),
                    direccion=request.POST.get('direccion'),
                    telefono_comercio=request.POST.get('telefono_comercio'),
                    tipo_comercio_id=request.POST.get('tipo_comercio'),
                    persona=persona
                )

            elif tipo == 'empresa':
                Empresas.objects.create(
                    nit=request.POST.get('nit'),
                    razon_social=request.POST.get('razon_social'),
                    codigo_ciiu=request.POST.get('codigo_ciiu'),
                    fecha_constitucion=request.POST.get('fecha_constitucion'),
                    direccion=request.POST.get('direccion'),
                    telefono_empresa=request.POST.get('telefono_empresa'),
                    tipo_empresa_id=request.POST.get('tipo_empresa'),
                    persona=persona
                )

            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Error en el registro: {str(e)}')
            return render(request, 'registro/registro.html', context)

    return render(request, 'registro/registro.html', context)