# Billetera Digital

Sistema de billetera digital desarrollado con Django que permite la gestión de usuarios, cuentas, bolsillos de ahorro, transferencias, notificaciones y auditoría de operaciones financieras.

---

# Tabla de Contenido

- [Descripción General](#descripción-general)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelo de Negocio](#modelo-de-negocio)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Base de Datos](#base-de-datos)
- [Ejecución](#ejecución)
- [Módulos del Sistema](#módulos-del-sistema)
- [Flujos Principales](#flujos-principales)
- [Rutas Disponibles](#rutas-disponibles)
- [Seguridad](#seguridad)
- [Auditoría](#auditoría)
- [Dependencias](#dependencias)
- [Mejoras Futuras](#mejoras-futuras)
- [Licencia](#licencia)

---

# Descripción General

Billetera Digital es una plataforma financiera desarrollada en Django que permite administrar cuentas virtuales, realizar transferencias entre usuarios, gestionar bolsillos de ahorro, consultar movimientos y recibir notificaciones sobre las operaciones realizadas.

La aplicación fue construida utilizando una arquitectura modular basada en dominios funcionales y una base de datos MySQL.

---

# Arquitectura del Proyecto

El sistema está organizado en los siguientes módulos:

| Módulo | Descripción |
|---------|-------------|
| Core | Configuración y catálogos generales |
| Usuarios | Gestión de clientes y perfiles |
| Autenticación | Login, sesiones y seguridad |
| Cuentas | Administración de cuentas y bolsillos |
| Transacciones | Transferencias y validaciones financieras |
| Notificaciones | Gestión de alertas y mensajes |
| Auditoría | Registro y trazabilidad de operaciones |

---

# Características

## Gestión de Usuarios

- Registro de usuarios.
- Inicio de sesión.
- Gestión de perfiles.
- Soporte para personas, empresas y comercios.

## Gestión de Cuentas

- Creación de cuentas asociadas a usuarios.
- Consulta de saldo disponible.
- Control de movimientos mensuales.
- Estado de cuenta.

## Bolsillos de Ahorro

- Creación de bolsillos.
- Consulta de saldo por bolsillo.
- Organización de fondos.

## Transferencias

- Transferencias entre cuentas.
- Validación de saldo disponible.
- Control de límites transaccionales.
- Aplicación automática de GMF.

## Notificaciones

- Registro de eventos.
- Consulta de notificaciones.
- Marcación de notificaciones leídas.

## Auditoría

- Registro de acciones críticas.
- Seguimiento de cambios.
- Almacenamiento de IP y usuario responsable.

---

# Tecnologías Utilizadas

| Tecnología | Versión |
|------------|----------|
| Python | 3.x |
| Django | 6.0.6 |
| MySQL | Compatible |
| python-decouple | 3.8 |
| mysqlclient | 2.2.8 |
| Argon2 | 25.1.0 |

---

# Estructura del Proyecto

```text
billetera-digital/
│
├── _config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
├── usuarios/
├── autenticacion/
├── cuentas/
├── transacciones/
├── notificaciones/
├── auditoria/
│
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── .env
```

---

# Modelo de Negocio

## Usuarios

El sistema permite administrar distintos tipos de clientes:

- Personas naturales.
- Empresas.
- Comercios.

## Cuenta Principal

Cada usuario posee una cuenta principal que almacena:

- Saldo disponible.
- Saldo total.
- Estado de cuenta.
- Movimientos realizados.

## Bolsillos

Los bolsillos permiten separar dinero para diferentes objetivos:

- Ahorro.
- Fondos de emergencia.
- Metas financieras.
- Organización de gastos.

---

# Instalación

## Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd billetera-digital
```

## Crear entorno virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Configuración

Crear un archivo `.env` en la raíz del proyecto.

```env
SECRET_KEY=tu_clave_secreta

DEBUG=True

DB_ENGINE=django.db.backends.mysql
DB_NAME=billetera_db
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
```

---

# Base de Datos

La aplicación utiliza MySQL como motor de persistencia.

## Entidades Principales

### Usuarios

- Usuarios
- Personas
- Empresas
- Comercios

### Autenticación

- Dispositivos
- Sesiones
- OTP

### Cuentas

- Cuentas
- Bolsillos

### Transacciones

- Transacciones
- Límites de transacción

### Notificaciones

- Notificaciones

### Auditoría

- Auditoría del sistema

> Nota: Los modelos fueron generados a partir de una base de datos existente y utilizan `managed = False`.

---

# Ejecución

## Aplicar migraciones

```bash
python manage.py migrate
```

## Iniciar servidor

```bash
python manage.py runserver
```

## Acceder al sistema

```text
http://127.0.0.1:8000
```

---

# Módulos del Sistema

## Usuarios

Responsable de:

- Registro de usuarios.
- Administración de perfiles.
- Gestión de personas, empresas y comercios.

## Autenticación

Responsable de:

- Inicio de sesión.
- Gestión de sesiones.
- Validación de credenciales.

### Seguridad

Las contraseñas son almacenadas utilizando:

```python
Argon2PasswordHasher
```

y validadas mediante:

```python
check_password()
```

## Cuentas

Permite:

- Consultar saldos.
- Administrar bolsillos.
- Gestionar cuentas.

### Servicios principales

```python
get_cuenta_usuario()
get_bolsillos()
get_saldo_total()
crear_cuenta()
crear_bolsillo()
```

## Transacciones

Gestiona:

- Transferencias.
- Límites transaccionales.
- Cálculo de GMF.

### Servicios principales

```python
transferir()
calcular_gmf()
aplica_gmf()
get_limite()
```

### Validaciones

- Verificación de saldo.
- Aplicación de impuestos.
- Registro de historial.
- Actualización de saldos.

## Notificaciones

Permite:

- Crear notificaciones.
- Consultar notificaciones.
- Marcar notificaciones como leídas.
- Contabilizar pendientes.

## Auditoría

Registra:

- Usuario responsable.
- Acción ejecutada.
- Tabla afectada.
- Dirección IP.
- Fecha y hora.
- Valores anteriores y nuevos.

---

# Flujos Principales

## Registro de Usuario

```text
Usuario
   ↓
Registro
   ↓
Creación de cuenta
   ↓
Acceso al sistema
```

## Inicio de Sesión

```text
Usuario
   ↓
Login
   ↓
Validación de credenciales
   ↓
Creación de sesión
   ↓
Dashboard
```

## Transferencia

```text
Cuenta origen
      ↓
Validación saldo
      ↓
Validación límite
      ↓
Cálculo GMF
      ↓
Registro transacción
      ↓
Actualización saldos
      ↓
Notificación
```

---

# Rutas Disponibles

## Autenticación

| Método | Endpoint |
|---------|----------|
| GET / POST | `/auth/login/` |
| GET | `/auth/logout/` |

## Usuarios

| Método | Endpoint |
|---------|----------|
| GET / POST | `/usuarios/registro/` |

## Cuentas

| Método | Endpoint |
|---------|----------|
| GET | `/cuentas/dashboard/` |
| GET | `/cuentas/bolsillos/` |
| GET | `/cuentas/cuentas/` |
| POST | `/cuentas/bolsillos/crear/` |
| POST | `/cuentas/bolsillos/eliminar/{id}/` |

## Transacciones

| Método | Endpoint |
|---------|----------|
| GET / POST | `/transacciones/transferir/` |
| GET | `/transacciones/historial/` |

## Notificaciones

| Método | Endpoint |
|---------|----------|
| GET | `/notificaciones/` |
| GET | `/notificaciones/{id}/leida/` |

---

# Seguridad

La plataforma incorpora:

- Hash de contraseñas mediante Argon2.
- Manejo seguro de sesiones.
- Validación de credenciales.
- Control de límites de transferencia.
- Prevención de operaciones duplicadas mediante Idempotency Key.
- Registro de auditoría para acciones críticas.

---

# Auditoría

Las operaciones importantes pueden registrarse mediante:

```python
registrar(
    accion,
    tabla_afectada,
    ip,
    usuario_id
)
```

Esto permite mantener trazabilidad completa de los cambios realizados dentro del sistema.

---

# Dependencias

```text
argon2-cffi==25.1.0
argon2-cffi-bindings==25.1.0
asgiref==3.11.1
cffi==2.0.0
Django==6.0.6
mysqlclient==2.2.8
pycparser==3.0
python-decouple==3.8
sqlparse==0.5.5
tzdata==2026.2
```

---

# Mejoras Futuras

- Implementación de autenticación OTP completa.
- API REST con Django REST Framework.
- JWT Authentication.
- Integración bancaria.
- Notificaciones por correo electrónico.
- Notificaciones SMS.
- Dashboard analítico.
- Docker.
- CI/CD.
- Cobertura de pruebas automatizadas.

---

# Licencia

Este proyecto se distribuye bajo la licencia que defina el propietario del repositorio.

Ejemplo:

```text
MIT License
```