from datetime import datetime
from .catalogos.estado_cliente import EstadoCliente
from .catalogos.roles import Roles
from .catalogos.tipo_cliente import TipoCliente
from .auditoria_sistema import caja_negra
import re
import hashlib
import secrets

class Cliente:
    """
    Representa un usuario dentro del sistema financiero.
    Gestiona validaciones de seguridad y estados de cuenta.
    """
    def __init__(self, email: str, contraseña: str, rol_id: int, estado_cliente_id: int, tipo_cliente_id: int, cliente_id: int = None):
        """
        inicializa un nuevo cliente, el id por defecto es None, si en caso tal no hay registro de el
        de mismo modo la fecha se asgina la actual, si esta registrado devuelve la original
        """
        self.cliente_id = cliente_id

        #Salt se inicializa vacio; el setter de contraseña lo generara
        self._salt = None

        #generacion interna y automatica
        self.__fecha_registro =  datetime.now()
        self._intentos_login = 3

        self.email = email
        self.contraseña = contraseña
        self.rol_id = rol_id
        self.estado_cliente_id = estado_cliente_id
        self.tipo_cliente_id = tipo_cliente_id

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self,email):
        #patron estandar para correos
        patron_gmail = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        try:
            if not isinstance(email,str) or not re.match(patron_gmail, email):
                raise ValueError(f"el formato de email {email} no es valido.")
            
            self._email = email
        except Exception as e:
            caja_negra.registrar_error("asignar Email", e)
            raise
    
    @property
    def contraseña(self):
        return self._contraseña
    
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
            if self._salt is None:
                self._salt = secrets.token_hex(16)  #genera 32 caracteres aleatorios

            #--- 3. ENCRIPTACION ---
            #guardamos el hash resultante de la clave + la "sal" del cliente
            self._contraseña = self.__encriptar_clave(nueva_contraseña, self._salt)
        except Exception as e:
            caja_negra.registrar_error("cambio de contraseña / hashing", e)
            raise

    @property
    def rol_id(self):
        return self._rol_id
    
    @rol_id.setter
    def rol_id(self, rol):
        try:
            if isinstance(rol, Roles):
                self._rol_id = rol
            else:
                raise ValueError(f"Rol {rol} no reconocido por el sistema.")
        except Exception as e:
            caja_negra.registrar_error("asignar rol", e)
            raise
    
    @property
    def estado_cliente_id(self):
        return self._estado_cliente_id
    
    @estado_cliente_id.setter
    def estado_cliente_id(self,estado):
        try:
            if isinstance(estado, EstadoCliente):
                self._estado_cliente_id = estado
            else:
                raise ValueError(f'Estado {estado} no reconocido por el sistema.')
        except Exception as e:
            caja_negra.registrar_error("asignar estado", e)
            raise
    
    @property
    def tipo_cliente_id(self):
        return self._tipo_cliente_id
    
    @tipo_cliente_id.setter
    def tipo_cliente_id(self, tipo_cliente):
        try:
            if isinstance(tipo_cliente, TipoCliente):
                self._tipo_cliente_id = tipo_cliente
            else:
                raise ValueError(f'Tipo de cliente {tipo_cliente} no reconocido por el sistema.')
        except Exception as e:
            caja_negra.registrar_error("asignar tipo de cliente", e)
            raise  

    def __str__(self):
        return f'Cliente(ID: {self.cliente_id}, Email: {self.email}, tipo de cliente: {self.tipo_cliente_id})'

    def verificar_credenciales(self, email_intento: str, pass_intento: str) -> bool:
        """verifica si el email y la contraseña coindiciden con las del cliente"""

        #1. validamos que la cuenta no este bloqueada
        if self.estado_cliente_id == EstadoCliente.BLOQUEADO:
            return False

        #2. validamos el email(texto plano contra texto plano)
        if self.email != email_intento:
            return False
        
        #3. se llama el metodo privado __encriptar_clave() para hashear esa contraseña
        # se convierte la contraseña que ingreso el usuario y la "sal" en un hash.
        hash_intento = self.__encriptar_clave(pass_intento, self._salt)

        #4. comparamos los dos hashes.
        if self._contraseña == hash_intento:
            #EXITO: se reinicia el contador de intentos para iniciar sesion
            self._intentos_login = 3
            return True
        else:
            #EROR: aqui se resta en 1 a los intentos para acceder a la cuenta(max 3 intentos)
            self._intentos_login -= 1

            #logica de bloqueo automatico
            if self._intentos_login <= 0:
                self.estado_cliente_id = EstadoCliente.BLOQUEADO  #se usa el setter para bloquear
                caja_negra.registrar_error(f"Seguridad - Bloqueo automatico", f"{self.email} por exceso de intentos")

            return False
        
    def suspender(self):
        """cambia el estado a suspendido, lo registra en historial"""
        self.estado_cliente_id = EstadoCliente.SUSPENDIDO

    def bloquear(self):
        """cambia el estado a bloqueado, lo registra en historial"""
        self.estado_cliente_id = EstadoCliente.BLOQUEADO

    def activar(self):
        """cambia el estado a activo, lo registra en historial"""
        self.estado_cliente_id = EstadoCliente.ACTIVO

    def desactivar(self):
        """cambia el estado a inactivo, lo registra en historial"""
        self.estado_cliente_id = EstadoCliente.INACTIVO

    @classmethod
    def cargar_cliente_db(cls, **datos):
        """
        Reconstruye un cliente a partir de los datos que ya estan en la BD.
        Aqui la contraseña ya es un hash y la "sal" ya existe.
        Evita volver a hashear la contraseña.
        """
        #creamos una instancia vacia sin pasar por el __init__ convencional
        cliente_existente = cls.__new__(cls)

        #se asigna directamente los valores a los atributos privados
        #saltandose los setters para no validar nada
        cliente_existente.cliente_id = datos["cliente_id"]
        cliente_existente._email = datos["email"]
        cliente_existente._contraseña = datos["contraseña"] # <- aqui ya viene la contraseña hasheada
        cliente_existente._salt = datos["salt"]             # la "sal" guardada
        cliente_existente._rol_id = datos["rol_id"]
        cliente_existente._estado_cliente_id = datos["estado_cliente_id"]
        cliente_existente._tipo_cliente_id = datos["tipo_cliente_id"]
        cliente_existente.__fecha_registro = datos["fecha_registro"]
        cliente_existente._intentos_login = 3

        return cliente_existente