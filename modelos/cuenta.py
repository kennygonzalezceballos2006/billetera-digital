from modelos.auditoria_sistema import caja_negra
from modelos.cliente import Cliente

# CLASE CUENTA
class Cuenta:
    def __init__(self, numero_cuenta, titular: Cliente, saldo_inicial=0):
        self.__numero_cuenta = numero_cuenta
        self._titular = titular
        self._saldo = saldo_inicial

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        try:
            if self._titular.estado == "Bloqueado":
                raise Exception("Usuario bloqueado")

            if monto <= 0:
                raise ValueError("Monto inválido")

            self._saldo += monto
            self._titular._historial_operaciones += 1
            self._titular.evaluar_cliente()

            print(f"Deposito realizado: {monto}\n su nuevo saldo es: {self._saldo}")
        except Exception as e:
            caja_negra.registrar_error("Depósito", e)
            print("Operación Denegada")

    def retirar(self, monto):
        try:
            if self._titular.estado == "Bloqueado":
                raise Exception("Usuario bloqueado")

            if monto <= 0:
                raise ValueError("Monto inválido")

            if monto > self._saldo:
                raise ValueError("Saldo insuficiente")

            self._saldo -= monto
            self._titular._historial_operaciones += 1
            self._titular.evaluar_cliente()

            print(f"Retiro realizado: {monto}\n su nuevo saldo es: {self._saldo}")
        except Exception as e:
            caja_negra.registrar_error("Retiro", e)
            print("Operación Denegada")

    def transferir(self, monto, cuenta_destino):
        try:
            if self._titular.estado == "Bloqueado":
                raise Exception("Usuario bloqueado")

            if cuenta_destino._titular.estado == "Bloqueado":
                raise Exception("Cuenta destino bloqueada")

            if monto <= 0:
                raise ValueError("Monto invalido")

            if monto > self._saldo:
                raise ValueError("Saldo insuficiente")

            self._saldo -= monto
            cuenta_destino.depositar(monto)

            self._titular._historial_operaciones += 1
            self._titular.evaluar_cliente()

            print(f"Transferencia realizada con un valor de: {monto}\n a la cuenta: {cuenta_destino}\n")
            print(f'su nuevo saldo es: {self._saldo}')
        except Exception as e:
            caja_negra.registrar_error("Transferencia", e)
            print("Operación Denegada")