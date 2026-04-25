from catalogos.tipo_documento import TipoDocumento
from utils.divipola import es_codigo_valido, obtener_nombre
import re

class PersonaNatural:
    def __init__(self, nombres: str, apellidos: str, telefono: str, tipo_documento: int, documento_identificacion: str, lugar_expedicion: str, fecha_expedicion: str, fecha_nacimiento: str, genero: int, cliente_id: int = None):
        self.__cliente_id = cliente_id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.tipo_documento = tipo_documento
        self.documento_identificacion = documento_identificacion
        self.lugar_expedicion = lugar_expedicion
        self.fecha_expedicion = fecha_expedicion
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
    
    #Getters para acceder mediante un metodo que actua como atributo
    #lee el valor del atributo y lo retorna
    @property
    def cliente_id(self):
        return self.__cliente_id

    @property
    def nombres(self):
        return self.__nombres
    
    @property
    def apellidos(self):
        return self.__apellidos
    
    @property
    def telefono(self):
        return self.__telefono
    
    @property
    def tipo_documento(self):
        return self.__tipo_documento
    
    @property
    def documento_identificacion(self):
        return self.__documento_identificacion
    
    @property
    def lugar_expedicion(self):
        return self.__lugar_expedicion
    
    @property
    def fecha_expedicion(self):
        return self.__fecha_expedicion
    
    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento
    
    @property
    def genero(self):
        return self.__genero
    
    #Setters para acceder y modificar el valor de un atributo privado mediante una logica de validacion
    #actua tanto para modificar como para insertar un valor a un atributo de una nueva instancia(PeronaNatural)
    @nombres.setter
    def nombres(self, nombres):
        #limpiamos la cadena de texto y colocamos en mayuscula la primera palabra de cada nombre
        nombres_limpios = nombres.strip().title()
        try:
            if len(nombres_limpios) > 3:
                raise ValueError("nombres demasiado cortos")
            
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombres_limpios):
                raise ValueError("los nombres solo pueden contener letras")
            
            self.__nombres = nombres_limpios
        except Exception as e:
            raise
    
    @apellidos.setter
    def apellidos(self, apellidos):
        #limpiamos la cadena de texto y colocamos en mayuscula la primera palabra de cada apellido
        apellidos_limpios = apellidos.strip().title()
        try:
            if len(apellidos_limpios) > 5:
                raise ValueError("apellidos demasiado cortos")
            
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos_limpios):
                raise ValueError("los apellidos solo pueden contener letras")
            
            self.__apellidos = apellidos_limpios
        except Exception as e:
            raise

    @telefono.setter
    def telefono(self, telefono):
        try:
            if not re.match(r'^3\d{9}$', telefono):
                raise ValueError('numero de telefono invalido')
            
            self.__telefono = telefono
        except Exception as e:
            raise

    @tipo_documento.setter
    def tipo_documento(self, tipo_documento):
        try:
            documento = tipo_documento.value if isinstance(tipo_documento, TipoDocumento) else tipo_documento

            if documento in [tipo.value for tipo in TipoDocumento]:
                self.__tipo_documento = documento
            else:
                raise ValueError(f"el documento ({documento}) no es reconocido por el sistema")
        except Exception as e:
            raise
    
    @documento_identificacion.setter
    def documento_identificacion(self, documento_identificacion):
        # mini diccionario para validar el formato del documento
        patrones = {
            1: r'^\d{6,10}$',         #cedula
            2: r'^\d{10,11}$',        # tarjeta de identidad
            3: r'^[a-zA-Z0-9]{5,9}$'  # pasaporte
        }
        # se obtiene el tipo de documento y lo busca en el mini diccionario
        patron = patrones.get(self.__tipo_documento)

        try:
            documento_limpio = documento_identificacion.strip()
            if not re.match(patron, documento_limpio):
                raise ValueError(f'formato de documento no valido para el tipo ({self.__tipo_documento})')
            
            self.__documento_identificacion = documento_limpio
        except Exception as e:
            raise
    
    