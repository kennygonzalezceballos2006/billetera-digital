from enum import Enum

class EstadoTransaccion(Enum):
    EXITOSA = 1
    FALLIDA = 2
    REVERTIDA = 3
    REVISION = 4
    PENDIENTE = 5