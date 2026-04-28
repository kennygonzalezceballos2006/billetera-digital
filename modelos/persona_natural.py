from catalogos.tipo_documento import TipoDocumento
from catalogos.generos import Genero
from utils.divipola import es_codigo_valido, obtener_departamento_y_municipio
from datetime import datetime
import re
import json

class PersonaNatural:
    def __init__(self,
                nombres: str,
                apellidos: str,
                telefono: str,
                tipo_documento: int,
                documento_identificacion: str,
                fecha_nacimiento: str,
                fecha_expedicion: str,
                lugar_expedicion: int,
                genero: int,
                cliente_id: int = None
            ):
        
        self.cliente_id = cliente_id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.tipo_documento = tipo_documento
        self.documento_identificacion = documento_identificacion
        self.lugar_expedicion = lugar_expedicion
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_expedicion = fecha_expedicion
        self.genero = genero
    
    #Getters para acceder mediante un metodo que actua como atributo
    #lee el valor del atributo y lo retorna
    @property
    def cliente_id(self):
        return self._cliente_id

    @property
    def nombres(self):
        return self._nombres
    
    @property
    def apellidos(self):
        return self._apellidos
    
    @property
    def telefono(self):
        return self._telefono
    
    @property
    def tipo_documento(self):
        return self._tipo_documento
    
    @property
    def documento_identificacion(self):
        return self._documento_identificacion
    
    @property
    def lugar_expedicion(self):
        return self._lugar_expedicion
    
    @property
    def fecha_expedicion(self):
        return self._fecha_expedicion
    
    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento
    
    @property
    def genero(self):
        return self._genero
    
    #Setters para acceder y modificar el valor de un atributo privado mediante una logica de validacion
    #actua tanto para modificar como para insertar un valor a un atributo de una nueva instancia(PeronaNatural)
    @cliente_id.setter
    def cliente_id(self, cliente_id):
        try:
            if getattr(self, '_cliente_id', None) is not None:
                raise ValueError("el id de este cliente ya fue registrado y no puede ser modificado")
            self._cliente_id = cliente_id
        except Exception as e:
            raise

    @nombres.setter
    def nombres(self, nombres):
        #limpiamos la cadena de texto y colocamos en mayuscula la primera palabra de cada nombre
        nombres_limpios = nombres.strip().title()
        try:
            if len(nombres_limpios) < 3:
                raise ValueError("nombres demasiado cortos")
            
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombres_limpios):
                raise ValueError("los nombres solo pueden contener letras")
            
            self._nombres = nombres_limpios
        except Exception as e:
            raise
    
    @apellidos.setter
    def apellidos(self, apellidos):
        #limpiamos la cadena de texto y colocamos en mayuscula la primera palabra de cada apellido
        apellidos_limpios = apellidos.strip().title()
        try:
            if len(apellidos_limpios) < 5:
                raise ValueError("apellidos demasiado cortos")
            
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos_limpios):
                raise ValueError("los apellidos solo pueden contener letras")
            
            self._apellidos = apellidos_limpios
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
    def tipo_documento(self, tipo_documento: int):
        try:
            if isinstance(tipo_documento, TipoDocumento):
                self._tipo_documento = tipo_documento
            elif isinstance(tipo_documento, int):
                resultado = next((t for t in TipoDocumento if t.id == tipo_documento), None)
                if resultado is None:
                    raise ValueError("Tipo de documento no reconocido")
                self._tipo_documento = resultado
            else:
                raise ValueError(f"tipo de documento no reconocido por el sistema")
        except Exception as e:
            raise
    
    @documento_identificacion.setter
    def documento_identificacion(self, documento_identificacion):
        try:
            #limpiamos la cadena de texto y sanitizamos la entrada
            documento_limpio = documento_identificacion.strip()

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
            
            self._documento_identificacion = documento_limpio
        except Exception as e:
            raise
    
    @lugar_expedicion.setter
    def lugar_expedicion(self, codigo_municipio):
        try:
            codigo_str = str(codigo_municipio).strip()
            #el frontend envio el codigo final tras elegir el Dpto y luego el municipio
            if es_codigo_valido(codigo_str):
                self._lugar_expedicion = codigo_str
            else:
                raise ValueError(f'municipio no reconocido por el sistema.')
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
            elif isinstance(genero, int):
                resultado = next((generos for generos in Genero if generos.value == genero), None)
                self._genero = resultado
                if resultado is None:
                    raise ValueError("genero no valido")
            else:
                raise ValueError('Genero no valido')
        except Exception as e:
            raise
    
    def __str__(self):
        datos = {
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "telefono": self.telefono,
            "tipo_documento": self.tipo_documento.name.replace("_", " "),
            "documento_identificacion": f"{int(self.documento_identificacion):,}".replace(",","."),
            "fecha_nacimiento": self.fecha_nacimiento,
            "lugar_expedicion": obtener_departamento_y_municipio(self.lugar_expedicion),
            "fecha_expedicion": self.fecha_expedicion,
            "genero": self.genero.name.replace("_", " "),
        }
        return json.dumps(datos, indent=10, ensure_ascii= False)

    def to_dict(self):
        return {
            "cliente_id": self._cliente_id,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "telefono": self.telefono,
            "tipo_documento": self.tipo_documento.name,
            "documento_identificacion": self.documento_identificacion,
            "fecha_nacimiento": self.fecha_nacimiento,
            "lugar_expedicion": obtener_departamento_y_municipio(self.lugar_expedicion),
            "fecha_expedicion": self.fecha_expedicion,
            "genero": self.genero.name,
        }
    
    @classmethod
    def cargar_persona_natural_bd(cls, **persona):

        persona_existente = cls.__new__(cls)

        persona_existente._nombres = persona["nombres"]
        persona_existente._apellidos = persona["apellidos"]
        persona_existente._telefono = persona["telefono"]
        persona_existente._tipo_documento = persona["tipo_documento"]
        persona_existente._documento_identificacion = persona["documento_identificacion"]
        persona_existente._fecha_nacimiento = persona["fecha_nacimiento"]
        persona_existente._lugar_expedicion = persona["lugar_expedicion"]
        persona_existente._fecha_expedicion = persona["fecha_expedicion"]
        persona_existente._genero = persona["genero"]

        return persona_existente

if __name__ == "__main__":
    persona_natural = PersonaNatural(
        "kenny gabriel",
        "gonzalez ceballos",
        "3016763302", 1,
        "1119393187",
        "2006-12-27",
        "2025-02-13",
        "44001",
        1 
        )
    print(persona_natural)