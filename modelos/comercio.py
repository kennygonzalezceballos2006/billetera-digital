from catalogos.tipo_documento import TipoDocumento
from catalogos.generos import Genero
from utils.divipola import es_codigo_valido
from datetime import datetime
import json
import re

class Comercio:
    def __init__(self,
                nombre_establecimiento: str,
                direccion: str,
                telefono: str,
                tipo_documento: int,
                documento_persona: str,
                lugar_expedicion: str,
                fecha_nacimiento: str,
                fecha_expedicion: str,
                genero: int,
                tipo_comercio: int,
                cliente_id: int = None
            ):
        
        self.cliente_id = cliente_id
        self.nombre_establecimiento = nombre_establecimiento
        self.direccion = direccion
        self.telefono = telefono
        self.tipo_documento = tipo_documento
        self.documento_persona = documento_persona
        self.lugar_expedicion = lugar_expedicion
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_expedicion = fecha_expedicion
        self.genero = genero
        self.tipo_comercio = tipo_comercio


    #propertys(Getters)
    #acceden y leen el valor del atributo sin la necesidad de acceder directamente al atributo
    @property
    def cliente_id(self):
        return self._cliente_id
    
    @property
    def nombre_establecimiento(self):
        return self._nombre_establecimiento
    
    @property
    def direccion(self):
        return self._direccion

    @property
    def telefono(self):
        return self._telefono
    
    @property
    def tipo_documento (self):
        return self._tipo_documento
    
    @property
    def documento_persona(self):
        return self._documento_persona
    
    @property
    def lugar_expedicion(self):
        return self._lugar_expedicion

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento
    
    @property
    def fecha_expedicion(self):
        return self._fecha_expedicion
    
    @property
    def genero(self):
        return self._genero

    @property
    def tipo_comercio(self):
        return self._tipo_comercio
    
    #Setters
    #acceden, modifican o asignan el valor a un atributo privado
    @cliente_id.setter
    def cliente_id(self, cliente_id):
        try:
            if getattr(self, '_cliente_id', None) is not None:
                raise ValueError("el id de este cliente ya fue registrado y no puede ser modificado")
            self._cliente_id = cliente_id
        except Exception as e:
            raise
    
    @nombre_establecimiento.setter
    def nombre_establecimiento(self, nombre_establecimiento: str):
        try:
            #limpiamos la cadena de texto para sanitizar la entrada
            nombre_establecimiento_limpio = nombre_establecimiento.strip()

            #verificamos que no sea una cadena de texto vacia
            if  not nombre_establecimiento_limpio.strip():
                raise ValueError("el nombre del establecimiento no puede estar vacio")
            
            #veificamos que el nombre tenga almenos 3 letras
            if len(nombre_establecimiento_limpio) < 3:
                raise ValueError(f"el nombre del establecimiento es demsiado corto. ({nombre_establecimiento})")
            
            #verificamos que el nombre no supere un limite real
            if len(nombre_establecimiento_limpio) > 100:
                raise ValueError("el nombre del establecimiento no puede superar 100 caracteres")
            
            #verificamos que el nombre cumpla con cierta logica dentro del nombre
            #que contenga desde a-z,A-Z,ñ,Ñ numeros0-9 y algunos caracteres especiales
            #si no cumple con ello lanzara un error especifico
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s&#\.]+$', nombre_establecimiento_limpio):
                raise ValueError("nombre no valido")
            
            #pasada la logica de validacion, asignamos el la cadena de texto
            #al atributo protegido
            self._nombre_establecimiento = nombre_establecimiento_limpio
        except Exception as e:
            raise
    
    @direccion.setter
    def direccion(self, direccion):
        try:
            #limpiamos la cadena de texto para sanitizar la entrada
            direccion_limpia = direccion.strip()

            #verificamos que la cadena de texto no este vacia
            if not direccion_limpia:
                raise ValueError("la direccion no puede estar vacia")
            
            #verificamos que la direccion tenga un minimo de caracteres
            if len(direccion_limpia) < 10:
                raise ValueError("la direccion proporcionada es demasiado corta")
            
            #verificamos que la direccion no supere un limite real
            if len(direccion_limpia) > 150:
                raise ValueError("la direccion no puede superar 150 caracteres")
            
            #verificamos que el nombre cumpla con cierta logica dentro del nombre
            #que contenga desde a-z,A-Z,ñ,Ñ numeros0-9 y algunos caracteres especiales
            #si no cumple con ello lanzara un error especifico
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s#\-\.,]+$', direccion_limpia):
                raise ValueError("direccion no valida")
            
            #pasada la logica de validacion, asignamos el la cadena de texto
            #al atributo protegido
            self._direccion = direccion_limpia
        except Exception as e:
            raise

    @telefono.setter
    def telefono(self, telefono):
        try:
            #limpiamos la cadena de texto para sanitizar la entrada
            telefono_limpio = telefono.strip()

            #verificamos que el telefono comience con 3 y tenga exactamente 10 digitos
            if not re.match(r'^3\d{9}$', telefono_limpio):
                raise ValueError('numero de telefono invalido')
            
            self._telefono = telefono_limpio
        except Exception as e:
            raise
    
    @tipo_documento.setter
    def tipo_documento(self, tipo_documento):
        try:
            if isinstance(tipo_documento, TipoDocumento):
                self._tipo_documento = tipo_documento
            else:
                raise ValueError(f"el documento ({tipo_documento}) no es reconocido por el sistema")
        except Exception as e:
            raise

    @documento_persona.setter
    def documento_persona(self, documento_persona):
        try:
            #verificamos que el documento no sea Tarjeta de identidad
            if self._tipo_documento == TipoDocumento.TARJETA_IDENTIDAD:
                raise ValueError("un menor de edad no puede ser representante de un comercio")
            
            #limpiamos la cadena de texto y sanitizamos la entrada
            documento_limpio = documento_persona.strip()

            #verificamos que el documento limpio no este vacio
            if not documento_limpio:
                raise ValueError("el documento no puede estar vacio")
            
            #verificamos que el documento no exceda el limite real
            if len(documento_limpio) > 15:
                raise ValueError("Documento no valido")
            
            #verficamos que el documento cumpla con el formato de su documento
            #mediante la libreria estandar re hacemos una compararcion para saber si cumple o no
            if not re.match(self._tipo_documento.patron, documento_limpio):
                raise ValueError(f'documento no valido')
            
            self._documento_persona = documento_limpio
        except Exception as e:
            raise
    
    @lugar_expedicion.setter
    def lugar_expedicion(self, codigo_municipio):
        try:
            #el frontend envio el codigo final tras elegir el Dpto y luego el municipio
            if es_codigo_valido(codigo_municipio):
                self._lugar_expedicion = codigo_municipio
            else:
                raise ValueError(f'el codigo DIVIPOLA {codigo_municipio} invalido.')
        except Exception as e:
            raise
    
    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento):
        try:
            #1 convertir el string a un objeto datetime
            nacimiento_dt = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            hoy = datetime.now()

            #calcular edad exacta
            edad = hoy.year - nacimiento_dt.year - ((hoy.month , hoy.day) < (nacimiento_dt.month, nacimiento_dt.day))

            #validaciones del negocio
            if nacimiento_dt > hoy:
                raise ValueError('la fecha de nacimiento no puede ser futura')
            
            if edad < 18:
                raise ValueError(f'el usuario debe ser mayor de edad, su edad actual es: {edad} años')
            
            if edad > 120:
                raise ValueError(f'fecha de nacimiento fuera del rango permitido')
            
            self._fecha_nacimiento = fecha_nacimiento
        except Exception as e:
            # Capturamos el error y lo relanzamos con un mensaje claro
            mensaje = str(e) if any(x in str(e) for x in ["años", "futura", "rango"]) else "Formato de fecha inválido (YYYY-MM-DD)"
            raise ValueError(mensaje)

    @fecha_expedicion.setter
    def fecha_expedicion(self, fecha_expedicion):
        try:
            expedicion_dt = datetime.strptime(fecha_expedicion, "%Y-%m-%d")
            
            # Validación: ¿Ya nació cuando sacó el documento?
            # Solo si ya tenemos la fecha de nacimiento asignada
            if hasattr(self, '_fecha_nacimiento'):
                nacimiento_dt = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
                if expedicion_dt <= nacimiento_dt:
                    raise ValueError("La fecha de expedición no puede ser anterior o igual a la de nacimiento")

            if expedicion_dt > datetime.now():
                raise ValueError('la fecha de expedicion no puede ser futura.')
            
            self._fecha_expedicion = fecha_expedicion
        except Exception as e:
            raise ValueError(str(e))
        
    @genero.setter
    def genero(self, genero):
        try:
            if isinstance(genero, Genero):
                self._genero = genero
            else:
                raise ValueError('Genero no valido')
        except Exception as e:
            raise
    
    def __str__(self):
        datos = {
            "nombre_establecimiento": self.nombre_establecimiento,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "tipo_documento": self.tipo_documento,
            "documento_persona": self.documento_persona,
            "lugar_expedicion": self.lugar_expedicion,
            "fecha_nacimiento": self.fecha_nacimiento,
            "fecha_expedicion": self.fecha_expedicion,
            "genero": self.genero,
            "tipo_comercio": self.tipo_comercio
        }
        return json.dumps(datos, indent=4, ensure_ascii= False)
    
    def to_dict(self):
         return {
             "cliente_id": self._cliente_id,
            "nombre_establecimiento": self.nombre_establecimiento,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "tipo_documento": self.tipo_documento,
            "documento_persona": self.documento_persona,
            "lugar_expedicion": self.lugar_expedicion,
            "fecha_nacimiento": self.fecha_nacimiento,
            "fecha_expedicion": self.fecha_expedicion,
            "genero": self.genero,
            "tipo_comercio": self.tipo_comercio
        }
    
    @classmethod
    def cargar_comercio_natural_bd(cls, **comercio):

        comercio_existente = cls.__new__(cls)

        comercio_existente._nombre_establecimiento = comercio["nombre_establecimiento"]
        comercio_existente._direccion = comercio["direccion"]
        comercio_existente._telefono = comercio["telefono"]
        comercio_existente._tipo_documento = comercio["tipo_documento"]
        comercio_existente._documento_persona = comercio["documento_persona"]
        comercio_existente._lugar_expedicion = comercio["lugar_expedicion"]
        comercio_existente._fecha_nacimiento = comercio["fecha_nacimiento"]
        comercio_existente._fecha_expedicion = comercio["fecha_expedicion"]
        comercio_existente._genero = comercio["genero"]
        comercio_existente._tipo_comercio = comercio["tipo_comercio"]

        return comercio_existente