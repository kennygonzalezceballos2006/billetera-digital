from modelos.auditoria_sistema import caja_negra
from datetime import datetime

# TRANSACCIONES
class Transaccion:
    def __init__(self, tipo, monto, cuenta_origen=None, cuenta_destino=None):
        self.__tipo = tipo
        self.__monto = monto
        self.__cuenta_origen = cuenta_origen
        self.__cuenta_destino = cuenta_destino
        self.__fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.__estado = "Pendiente"

    @property
    def tipo(self):
        return self.__tipo

    @property
    def monto(self):
        return self.__monto

    def concretar(self):
        try:
            if self.__tipo not in ['Deposito','Retiro','Transferencia']:
                raise ValueError("Tipo invalido")

            if not isinstance(self.__monto, (int, float)) or self.__monto <= 0:
                raise ValueError("Monto invalido")

            if self.__tipo == 'Deposito':
                if self.__cuenta_destino is None:
                    raise ValueError("Cuenta destino requerida")
                self.__cuenta_destino.depositar(self.__monto)

            if self.__tipo == 'Retiro':
                self.__cuenta_origen.retirar(self.monto)

            if self.__tipo == 'Transferencia':
                if self.__cuenta_origen == self.__cuenta_destino:
                    raise ValueError("no se puede transferir a la misma cuenta")
                
                elif self.__cuenta_origen is None or self.__cuenta_destino is None:
                    raise ValueError("Cuenta origen y destino requeridas")
                self.__cuenta_origen.transferir(self.__monto, self.__cuenta_destino)

            self.__estado = "Completada"

        except Exception as e:
            self.__estado = "Fallida"
            caja_negra.registrar_error("Concretar transaccion", e)
            print("Operación Denegada")