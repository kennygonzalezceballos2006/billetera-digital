from datetime import datetime

class HistorialCuenta:
    def __init__(self, descripcion: str, cuenta_id: int, monto: float = None, saldo_restante: float = None, historial_id: int = None):
        self.__historial_id = historial_id
        self.__descripcion = descripcion
        self.__monto = monto
        self.__saldo_restante = saldo_restante
        self.__cuenta_id = cuenta_id
        self.__fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    @property
    def historial_id(self):
        return self.__historial_id
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def monto(self):
        return self.__monto
    
    @property
    def saldo_restante(self):
        return self.__saldo_restante
    
    @property
    def cuenta_id(self):
        return self.__cuenta_id
    
    @property
    def fecha_hora(self):
        return self.__fecha_hora
    
    def __str__(self):
        return(f'historial:{self.__historial_id},cuenta:{self.__cuenta_id},descripcion:{self.__descripcion},monto:{self.__monto},saldo restante:{self.__saldo_restante}')
    
    @classmethod
    def cargar_historial_bd(cls, **datos):
        #creamos una instancia "vacia" sin pasar por el __init__ convencional
        registro_existente = cls.__new__(cls)

        #se asigna automaticamente los valores a los atributos privados
        registro_existente._HistorialCuenta__historial_id = datos["historial_id"]
        registro_existente._HistorialCuenta__cuenta_id = datos["cuenta_id"]
        registro_existente._HistorialCuenta__fecha_hora = datos["fecha_hora"]
        registro_existente._HistorialCuenta__descripcion = datos["descripcion"]
        registro_existente._HistorialCuenta__monto = datos["monto"]
        registro_existente._HistorialCuenta__saldo_restante = datos["saldo_restante"]

        return registro_existente