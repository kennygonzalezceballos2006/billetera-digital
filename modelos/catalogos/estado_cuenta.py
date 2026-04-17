from enum import Enum

class EstadoCuenta(Enum):
    ACTIVA = 1
    BLOQUEADA = 2
    SUSPENDIDA = 3
    INACTIVA = 4