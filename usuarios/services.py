# usuarios/services.py
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from core.models import Catalogos
from .models import Usuarios, Personas, Comercios, Empresas

def crear_usuario(email, password, tipo):
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
    return Usuarios.objects.create(
        email=email,
        password_hash=make_password(password),
        fecha_registro=timezone.now(),
        rol=rol_usuario,
        estado_cliente=estado_activo,
        tipo_cliente=tipo_cliente
    )

def crear_persona(datos, usuario):
    return Personas.objects.create(
        nombres=datos.get('nombres'),
        apellidos=datos.get('apellidos'),
        telefono=datos.get('telefono'),
        identificacion=datos.get('identificacion'),
        fecha_nacimiento=datos.get('fecha_nacimiento'),
        fecha_expedicion_documento=datos.get('fecha_expedicion_documento'),
        pais_nacimiento_id=datos.get('pais_nacimiento'),
        municipio_nacimiento_id=datos.get('municipio_nacimiento'),
        lugar_expedicion_documento_id=datos.get('lugar_expedicion_documento'),
        sexo_id=datos.get('sexo'),
        tipo_documento_id=datos.get('tipo_documento'),
        usuario=usuario
    )

def crear_comercio(datos, persona):
    return Comercios.objects.create(
        nombre_establecimiento=datos.get('nombre_establecimiento'),
        direccion=datos.get('direccion'),
        telefono_comercio=datos.get('telefono_comercio'),
        tipo_comercio_id=datos.get('tipo_comercio'),
        persona=persona
    )

def crear_empresa(datos, persona):
    return Empresas.objects.create(
        nit=datos.get('nit'),
        razon_social=datos.get('razon_social'),
        codigo_ciiu=datos.get('codigo_ciiu'),
        fecha_constitucion=datos.get('fecha_constitucion'),
        direccion=datos.get('direccion'),
        telefono_empresa=datos.get('telefono_empresa'),
        tipo_empresa_id=datos.get('tipo_empresa'),
        persona=persona
    )

def email_existe(email):
    return Usuarios.objects.filter(email=email).exists()

def identificacion_existe(identificacion):
    return Personas.objects.filter(identificacion=identificacion).exists()

def get_context_registro():
    return {
        'tipos_documento': Catalogos.objects.filter(categoria__categoria_nombre='tipo_documento'),
        'sexos': Catalogos.objects.filter(categoria__categoria_nombre='sexo'),
        'municipios': Catalogos.objects.filter(categoria__categoria_nombre='municipio'),
        'tipos_comercio': Catalogos.objects.filter(categoria__categoria_nombre='tipo_comercio'),
        'tipos_empresa': Catalogos.objects.filter(categoria__categoria_nombre='tipo_empresa'),
        'paises': Catalogos.objects.filter(categoria__categoria_nombre='pais'),
    }

def registrar(datos, tipo, email, password):
    usuario = crear_usuario(email, password, tipo)
    persona = crear_persona(datos, usuario)
    if tipo == 'comercio':
        crear_comercio(datos, persona)
    elif tipo == 'empresa':
        crear_empresa(datos, persona)
    return usuario