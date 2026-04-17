from datetime import datetime
import re
from catalogos.estado_cliente import EstadoCliente
from auditoria_sistema import caja_negra

class Cliente:
    """
    Representa un usuario dentro del sistema financiero.
    Gestiona validaciones de seguridad y estados de cuenta.
    """
    def __init__(self, email: str, contraseña: str, rol_id: int, estado_cliente_id: int, tipo_cliente_id: int, cliente_id: int = None, fecha_registro = None):
        """
        inicializa un nuevo cliente, el id por defecto es None, si en caso tal no hay registro de el
        de mismo modo la fecha se asgina la actual, si esta registrado devuelve la original
        """
        self.__cliente_id = cliente_id
        self.__email = email
        self.__contraseña = contraseña
        self.__rol_id = rol_id
        self.__estado_cliente_id = estado_cliente_id
        self.__tipo_cliente_id = tipo_cliente_id
        self.__fecha_registro = fecha_registro if fecha_registro else datetime.now()
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self,nuevo_email):
        try:
            if not isinstance(nuevo_email,str) or "@" not in nuevo_email:
                raise ValueError("email no valido")
            
            self.__email = nuevo_email
        except Exception as e:
            caja_negra.registrar_error("asignar Email", e)
    
    @property
    def contraseña(self):
        return self.__contraseña
    
    @contraseña.setter
    def contraseña(self, nueva_contraseña):
        try:
            if not isinstance(nueva_contraseña, str) or not nueva_contraseña.strip():
                raise ValueError("Contraseña inválida")
            if not re.search(r'[A-Z]', nueva_contraseña):
                raise ValueError("Debe tener al menos una mayúscula")
            if not re.search(r'[a-z]', nueva_contraseña):
                raise ValueError("Debe tener al menos una minúscula")
            if not re.search(r'[0-9]', nueva_contraseña):
                raise ValueError("Debe tener al menos un número")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', nueva_contraseña):
                raise ValueError("Debe tener al menos un carácter especial")
            if len(nueva_contraseña) < 8:
                raise ValueError("Mínimo 8 caracteres")
            self.__contraseña = nueva_contraseña
        except Exception as e:
            caja_negra.registrar_error("cambio de contraseña", e)
    
    @property
    def rol_id(self):
        return self.__rol_id
    
    @property
    def estado_cliente_id(self):
        return self.__estado_cliente_id
    
    @estado_cliente_id.setter
    def estado_cliente_id(self,nuevo_estado):
        try:
            if nuevo_estado in [EstadoCliente.ACTIVO, EstadoCliente.INACTIVO, EstadoCliente.SUSPENDIDO, EstadoCliente.BLOQUEADO]:
                self.__estado_cliente_id = nuevo_estado
            else:
                raise ValueError("estado invalido")
        except Exception as e:
            caja_negra.registrar_error("asignar estado", e)
    
    @property
    def tipo_cliente_id(self):
        return self.__tipo_cliente_id

    def __str__(self):
        return f'Cliente(ID: {self.__cliente_id}, Email: {self.__email}, tipo de cliente: {self.__tipo_cliente_id})'