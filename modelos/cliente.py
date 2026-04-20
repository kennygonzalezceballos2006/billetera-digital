from datetime import datetime
import re
from .catalogos.estado_cliente import EstadoCliente
from .catalogos.roles import Roles
from .catalogos.tipo_cliente import TipoCliente
import secrets
import hashlib
from .auditoria_sistema import caja_negra

class Cliente:
    """
    Representa un usuario dentro del sistema financiero.
    Gestiona validaciones de seguridad y estados de cuenta.
    """
    def __init__(self, email: str, contraseña: str, rol_id: Roles, estado_cliente_id: EstadoCliente, tipo_cliente_id: TipoCliente, cliente_id: int = None):
        """
        inicializa un nuevo cliente, el id por defecto es None, si en caso tal no hay registro de el
        de mismo modo la fecha se asgina la actual, si esta registrado devuelve la original
        """
        self.__cliente_id = cliente_id

        #Salt se inicializa vacio; el setter de contraseña lo generara
        self.__salt = None

        #generacion interna y automatica
        self.__fecha_registro =  datetime.now()
        self.__intentos_login = 3

        self.email = email
        self.contraseña = contraseña
        self.rol_id = rol_id
        self.estado_cliente_id = estado_cliente_id
        self.tipo_cliente_id = tipo_cliente_id

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
            raise
    
    @property
    def contraseña(self):
        return self.__contraseña
    
    @staticmethod
    def __encriptar_clave(password_en_texto_plano: str, salt: str) -> str:
        """
        recibe la contraseña tal cual la escribio el usuario
        y la devuelve convertida en un hash SHA-256
        """
        #se combina la contraseña con la "sal"(esto se llama 'salting')
        contraseña_con_salt = password_en_texto_plano + salt

        #.encode() convierte el texto a bytes(es necesario para el hashlib)
        #.hexdigest() convierte el resultado de los bytes a una cadena de texto legible
        return hashlib.sha256(contraseña_con_salt.encode()).hexdigest()
    
    @contraseña.setter
    def contraseña(self, nueva_contraseña):
        try:
            #--- 1. VALIDACIONES DE SEGURIDAD (LOS REGEX) ---
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

            #--- 2. GESTION DEL SALT ---
            #si el atributo __salt es None (Usuario nuevo), generamos uno
            if self.__salt is None:
                self.__salt = secrets.token_hex(16)  #genera 32 caracteres aleatorios

            #--- 3. ENCRIPTACION ---
            #guardamos el hash resultante de la clave + la "sal" del cliente
            self.__contraseña = self.__encriptar_clave(nueva_contraseña, self.__salt)
        except Exception as e:
            caja_negra.registrar_error("cambio de contraseña / hashing", e)
            raise

    @property
    def rol_id(self):
        return self.__rol_id
    
    @rol_id.setter
    def rol_id(self, nuevo_rol):
        try:
            #se extra el valor si nos pasan el enum completo
            rol = nuevo_rol.value if isinstance(nuevo_rol, Roles) else nuevo_rol

            #lista de valores validos (1, 2, 3)
            if rol in [roles.value for roles in Roles]:
                self.__rol_id = rol
            else:
                raise ValueError(f"Rol {rol} no reconocido por el sistema.")
        except Exception as e:
            caja_negra.registrar_error("asignar rol", e)
            raise
    
    @property
    def estado_cliente_id(self):
        return self.__estado_cliente_id
    
    @estado_cliente_id.setter
    def estado_cliente_id(self,nuevo_estado):
        try:
            #se extra el valor si nos pasan el enum completo
            estado = nuevo_estado.value if isinstance(nuevo_estado, EstadoCliente) else nuevo_estado

            #lista de valores validos (1, 2, 3, 4)
            if estado in [estados.value for estados in EstadoCliente]:
                self.__estado_cliente_id = estado
            else:
                raise ValueError(f'Estado {estado} no reconocido por el sistema.')
        except Exception as e:
            caja_negra.registrar_error("asignar estado", e)
            raise
    
    @property
    def tipo_cliente_id(self):
        return self.__tipo_cliente_id
    
    @tipo_cliente_id.setter
    def tipo_cliente_id(self, nuevo_tipo_cliente):
        try:
            #se extra el valor si nos pasan el enum completo
            tipo_cliente = nuevo_tipo_cliente.value if isinstance(nuevo_tipo_cliente, TipoCliente) else nuevo_tipo_cliente

            #lista de valores validos (1, 2, 3)
            if tipo_cliente in [tipos.value for tipos in TipoCliente]:
                self.__tipo_cliente_id = tipo_cliente
            else:
                raise ValueError(f'Tipo de cliente {tipo_cliente} no reconocido por el sistema.')
        except Exception as e:
            caja_negra.registrar_error("asignar tipo de cliente", e)
            raise  

    def __str__(self):
        return f'Cliente(ID: {self.__cliente_id}, Email: {self.__email}, tipo de cliente: {self.__tipo_cliente_id})'

    def verificar_credenciales(self, email_intento: str, pass_intento: str) -> bool:
        """verifica si el email y la contraseña coindiciden con las del cliente"""

        #1. validamos el email(texto plano contra texto plano)
        if self.email != email_intento:
            return False
        
        #2. se llama el metodo privado __encriptar_clave() para hashear esa contraseña
        # se convierte la contraseña que ingreso el usuario y la "sal" en un hash.
        hash_intento = self.__encriptar_clave(pass_intento, self.__salt)

        #3. comparamos los dos hashes.
        if self.__contraseña == hash_intento:
            #EXITO: se reinicia el contador de intentos para iniciar sesion
            self.__intentos_login = 3
            return True
        else:
            #EROR: aqui se resta en 1 a los intentos para acceder a la cuenta(max 3 intentos)
            self.__intentos_login -= 1

            #logica de bloqueo automatico
            if self.__intentos_login <= 0:
                self.estado_cliente_id = EstadoCliente.BLOQUEADO.value  #se usa el setter para bloquear
                caja_negra.registrar_error(f"Seguridad - Bloqueo automatico", f"{self.email} por exceso de intentos")

            return False
        
    def suspender_cuenta(self):
        """cambia el estado a suspendido, lo registra en auditoria del sistema y historial de cuenta"""
        self.__estado_cliente_id = EstadoCliente.SUSPENDIDO.value

    @classmethod
    def cargar_cliente_db(cls, email, contraseña, rol_id, estado_cliente_id, tipo_cliente_id, cliente_id, fecha_registro, salt):
        """
        Reconstruye un cliente a partir de los datos que ya estan en la BD.
        Aqui la contraseña ya es un hash y la "sal" ya existe.
        Evita volver a hashear la contraseña.
        """
        #creamos una instancia vacia sin pasar por el __init__ convencional
        cliente_existente = cls.__new__(cls)

        #se asigna directamente los valores a los atributos privados
        #saltandose los setters para no validar nada
        cliente_existente._Cliente__cliente_id = cliente_id
        cliente_existente._Cliente__email = email
        cliente_existente._Cliente__contraseña = contraseña # <- aqui ya viene la contraseña hasheada
        cliente_existente._Cliente__salt = salt             # la "sal" guardada
        cliente_existente._Cliente__rol_id = rol_id
        cliente_existente._Cliente__estado_cliente_id = estado_cliente_id
        cliente_existente._Cliente__tipo_cliente_id = tipo_cliente_id
        cliente_existente._Cliente__fecha_registro = fecha_registro
        cliente_existente._Cliente__intentos_login = 3

        return cliente_existente