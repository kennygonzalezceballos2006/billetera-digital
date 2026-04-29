from catalogos.tipo_documento import TipoDocumento
from catalogos.tipos_empresas import TipoEmpresa
import re

class Empresa:
    def __init__(self,
                    nit: str,
                    razon_social: str,
                    tipo_empresa: int,
                    codigo_ciiu: str,
                    fecha_constitucion: str,
                    direccion: str,
                    ciudad: str,
                    telefono: str,
                    representante_nombres: str,
                    representante_apellidos: str,
                    genero_representante: str,
                    tipo_documento_representante: int,
                    documento_representante: str,
                    lugar_expedicion_representante: str,
                    fecha_nacimiento_representante: str,
                    fecha_expedicion_representante: str,
                    cliente_id: int = None,
                ):
        self.cliente_id = cliente_id
        self.nit = nit
        self.razon_social = razon_social
        self.tipo_empresa = tipo_empresa
        self.codigo_ciiu = codigo_ciiu
        self.fecha_constitucion = fecha_constitucion
        self.direccion = direccion
        self.ciudad = ciudad
        self.telefono = telefono
        self.representante_nombres = representante_nombres
        self.representante_apellidos = representante_apellidos
        self.genero_representante = genero_representante
        self.tipo_documento_representante = tipo_documento_representante
        self.documento_representante = documento_representante
        self.lugar_expedicion_representante = lugar_expedicion_representante
        self.fecha_nacimiento_representante = fecha_nacimiento_representante
        self.fecha_expedicion_representante = fecha_expedicion_representante

    #propertys
    @property
    def cliente_id(self):
        return self._cliente_id
    
    @property
    def nit(self):
        return self._nit
    
    @property
    def razon_social(self):
        return self._razon_social
    
    @property
    def tipo_empresa(self):
        return self._tipo_empresa
    
    @property
    def codigo_ciiu(self):
        return self._codigo_ciiu
    
    @property
    def fecha_constitucion(self):
        return self._fecha_constitucion
    
    @property
    def direccion(self):
        return self._direccion
    
    @property
    def ciudad(self):
        return self._ciudad
    
    @property
    def telefono(self):
        return self._telefono
    
    @property
    def representante_nombres(self):
        return self._representante_nombres
    
    @property
    def representante_apellidos(self):
        return self._representante_apellidos
    
    @property
    def genero_representante(self):
        return self._genero_representante
    
    @property
    def tipo_documento_representante(self):
        return self._tipo_documento_representante
    
    @property
    def documento_representante(self):
        return self._documento_representante
    
    @property
    def lugar_expedicion_representante(self):
        return self._lugar_expedicion_representante
    
    @property
    def fecha_nacimiento_representante(self):
        return self._fecha_nacimiento_representante
    
    @property
    def fecha_expedicion_representante(self):
        return self._fecha_expedicion_representante
    
    #setters
    @cliente_id.setter
    def cliente_id(self, cliente_id):
        try:
            if getattr(self, '_cliente_id', None) is not None:
                raise ValueError("el id de este cliente ya fue registrado y no puede ser modificado")
            self._cliente_id = cliente_id
        except Exception as e:
            raise

    @nit.setter
    def nit(self, nit: str):
        try:
            #limpiamos la cadena de texto y sanitizamos la entrada
            nit_limpio = nit.strip()

            #verificamos que no este vacio el nit
            if not nit_limpio:
                raise ValueError("el NIT no puede estar vacio")
            
            #verificamos que cumpla con un formato para NITs
            if not re.match(r'^\d{9}-\d{1}$', nit_limpio):
                raise ValueError("NIT no valido")
            
            #asignamos el nit limpio y validado al atributo
            self._nit = nit_limpio
        except Exception as e:
            raise
    
    @razon_social.setter
    def razon_social(self, razon_social: str):
        try:
            #limpiamos la cadena de texto y sanitizamos la entrada
            razon_social_limpia = razon_social.strip().upper()

            #verificamos que no este vacio
            if not razon_social_limpia:
                raise ValueError("la razon social no puede estar vacia")
            
            #verificamos que no sea demasiado corta
            if len(razon_social_limpia) < 3:
                raise ValueError("la razon social es demasiado corta")
            
            #verificamos que no supere un limite real
            if len(razon_social_limpia) > 150:
                raise ValueError("la razon social no puede superar los 150 caracteres")
            
            #verificamos que contenga caracteres anormales
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s%\.\-]+$', razon_social_limpia):
                raise ValueError("razon social no valida")
            
            #asignamos la razon social limpia y validada al atributo
            self._razon_social = razon_social_limpia
        except Exception as e:
            raise

    @tipo_empresa.setter
    def tipo_empresa(self, tipo_empresa):
        try:
            if isinstance(tipo_empresa, TipoEmpresa):
                self._tipo_empresa = tipo_empresa
            elif isinstance(tipo_empresa, int):
                resultado = next((tipo for tipo in TipoEmpresa if tipo.value == tipo_empresa), None)
                self._tipo_empresa = resultado
                if resultado is None:
                    raise ValueError("tipo de empresa no valida")
            else:
                raise ValueError("tipo de empresa no valida")
        except Exception as e:
            raise
    