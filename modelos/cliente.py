from modelos.auditoria_sistema import caja_negra

# CLASE CLIENTE
class Cliente:
    def __init__(self, nombre, documento, fecha_nacimiento, telefono, email):
        self.__nombre = nombre
        self.__documento = documento
        self.__fecha_nacimiento = fecha_nacimiento
        self.__telefono = telefono
        self.__email = email
        self._cuentas = []

        self.estado = "Activo"
        self._historial_operaciones = 0

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        try:
            if isinstance(valor, str) and valor.strip():
                self.__nombre = valor
            else:
                raise ValueError("Nombre invalido")
        except Exception as e:
            caja_negra.registrar_error("Asignar nombre", e)
            print("Operación Denegada")

    def agregar_cuenta(self, cuenta):
        self._cuentas.append(cuenta)

    def evaluar_cliente(self):
        if self._historial_operaciones >= 3 and self.estado == "Activo":
            self.estado = "VIP"
            print(f"{self.__nombre} ahora es VIP")
        else:
            print(f"{self.__nombre} sigue siendo {self.estado}")