from datetime import datetime

# CAJA NEGRA (REGISTRO OCULTO DE ERRORES)
class CajaNegra:
    def __init__(self):
        self._errores = []

    def registrar_error(self, operacion, motivo):
        self._errores.append({
            "operacion": operacion,
            "motivo": str(motivo),
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
    
    def mostrar_errores(self):
        for error in self._errores:
            print(f'fecha: {error["fecha"]} | motivo: {error["motivo"]} | operacion: {error["operacion"]}')

caja_negra = CajaNegra()