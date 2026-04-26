from enum import Enum

class TipoDocumento(Enum):
    CEDULA_CIUDADANIA = (1, r'^\d{6,10}$')                        # CC — Cédula de Ciudadanía
    CEDULA_EXTRANJERA = (2, r'^\d{6,7}$')                         # CE — Cédula de Extranjería
    PERMISO_ESPECIAL_DE_PERMANENCIA = (3, r'^PE[a-zA-Z0-9]{9}$')  # PEP — empieza con PE + 9 caracteres
    PERMISO_DE_PROTECCION_TEMPORAL = (4, r'^[a-zA-Z0-9]{1,15}$')  # PPT — alfanumérico hasta 15 caracteres
    PASAPORTE = (5, r'^[a-zA-Z0-9]{5,9}$')                        # Pasaporte
    TARJETA_IDENTIDAD = (6, r'^\d{10,11}$')                       # TI — Tarjeta de Identidad

    #mediante el init desempaquetamos el enum que es una tupla
    def __init__(self, id, patron):
        self.id = id
        self.patron = patron