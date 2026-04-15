from modelos.transaccion import Transaccion

#CONTROL DE TRANSACCIONES
class ControlTransacciones:
    def __init__(self):
        self._historial = []

    def ejecutar_transaccion(self, transaccion: Transaccion):
        transaccion.concretar()
        self._historial.append(transaccion)

    def procesar_lote(self, lista_transacciones):
        exitosas = 0
        fallidas = []

        for t in lista_transacciones:
            t.concretar()
            self._historial.append(t)

            if t.__estado == "Completada":
                exitosas += 1
            else:
                fallidas.append(t)

        print("\n=== REPORTE LOTE ===")
        print(f"Exitosas: {exitosas}")
        print(f"Fallidas: {len(fallidas)}")

        for f in fallidas:
            print(f"Falló: {f.tipo} de {f.monto}")

    def mostrar_historial(self):
        print("\n=== HISTORIAL DE TRANSACCIONES ===")
        for t in self._historial:
            print(f"{t.tipo} de {t.monto} - Estado: {t._Transaccion__estado}")