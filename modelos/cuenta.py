from catalogos.estado_cuenta import EstadoCuenta
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from modelos.auditoria_sistema import caja_negra

# CLASE CUENTA
class Cuenta:
    # se aplica un metodo estatico para generar la cuenta sin nececidad de un parametro
    # y la clase cuenta no debe recibir numero_cuenta como parametro, ya que esta misma se encarga de ello
    # creamos el meotodo estatico dentro de la clase para que no este suelto, sino que sea parte de la clase
    @staticmethod
    def generar_numero_cuenta():
        #se genera una variable que captura la hora y fecha exacta de la creacion de la cuenta
        #de ahi generaremos la cuenta
        ahora = datetime.now()
        #se utiliza la hora y minuto, luego los primeros 3 digitos
        #ej:(1423) -> se extrae 142
        oficina = ahora.strftime("%H%M")[:3]
        #se utiliza el año, mes y dia. luego los ultimos 6 digitos
        #ej:(20260420) -> se extrae 260420
        secuencia = ahora.strftime("%Y%m%d")[-6:]
        # se utilizan los segundos. se trabaja con los 2 digitos
        #ej:(27) -> se extrae 27
        control = ahora.strftime("%S")
        #lo cual nos retornara algo parecido:
        #ej:"142-260620-27"
        return f'{oficina}-{secuencia}-{control}'

    def __init__(self, cliente_id: int, estado_cuenta_id: int, saldo=0,cuenta_id: int = None):
        self.__cliente_id = cliente_id
        self.estado_cuenta = estado_cuenta_id
        self.__numero_cuenta = Cuenta.generar_numero_cuenta()
        self.__fecha_creacion = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.__cuenta_id = cuenta_id
        self.__saldo = Decimal('0')

    #decoradores para cada atributo del objeto
    @property
    def cliente_id(self):
        return self.__cliente_id
    
    @property
    def numero_cuenta(self):
        return self.__numero_cuenta
    
    @property
    def fecha_creacion(self):
        return self.__fecha_creacion
    
    @property
    def cuenta_id(self):
        return self.__cuenta_id

    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def estado_cuenta(self):
        return self.__estado_cuenta
    

    #setters
    @cuenta_id.setter
    def cuenta_id(self, cuenta_id):
        if self.__cuenta_id is not None:
            raise ValueError("el cuenta_id ya fue registrado y no puede modificarse")
        self.__cuenta_id = cuenta_id

    @estado_cuenta.setter
    def estado_cuenta(self,estado_cuenta_id):
        try:
            #se extrae el valor del argumento y se verifica que exista en el modulo de EstadoCuenta
            #si no existe se crea un nuevo estado
            estado_cuenta = estado_cuenta_id.value if isinstance(estado_cuenta_id, EstadoCuenta) else estado_cuenta_id
            
            #se recorre los valores de EstadoCuenta y se verifica que exista
            if estado_cuenta in [estado.value for estado in EstadoCuenta]:
                self.__estado_cuenta = estado_cuenta
            else:
                #si no existe lanza devuelve un error controlado
                raise ValueError(f'estado {estado_cuenta} no reconocido por el sistema')
        except Exception as e:
            caja_negra.registrar_error("asignar estado", e)
            raise
    
    #metodos para cambiar el estado de una cuenta
    def bloquear(self):
        """cambia el estado a bloqueada, lo registra en historial de cuenta"""
        self.estado_cuenta = EstadoCuenta.BLOQUEADA.value
    
    def activar(self):
        """cambia el estado a activa, lo registra en historial de cuenta"""
        self.estado_cuenta = EstadoCuenta.ACTIVA.value
    
    def suspender(self):
        """cambia el estado a suspendida, lo registra en historial de cuenta"""
        self.estado_cuenta = EstadoCuenta.SUSPENDIDA.value
    
    def desactivar(self):
        """cambia el estado a inactiva, lo registra en historial de cuenta"""
        self.estado_cuenta = EstadoCuenta.INACTIVA.value

    #metodos para sumar y restar al saldo
    def depositar(self, monto: float):
        try:
            #logia de validacion antes de depositar el dinero
            #verificar que la cuenta este activa
            if self.__estado_cuenta != EstadoCuenta.ACTIVA.value:
                raise ValueError(f"el estado de la cuenta no permite depositar. ({self.__estado_cuenta})")
            
            #verificar que no sea un bool
            if isinstance(monto, bool):
                raise ValueError("el monto no puede ser booleano")
            
            #verificar que el monto sea numerico
            if not isinstance(monto, (int, float)):
                raise TypeError(f"el monto debe ser un valor numerico. ({monto})")
            
            #aplicando el estandar bancario y evitando los errores del float
            #se implementa la libreria Decimal
            monto = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            #mayor a 0
            if monto <= 0:
                raise ValueError(f"el monto debe ser mayor a 0({monto})")

            #monto minimo
            if monto < 1000:
                raise ValueError(f"el monto minimo para depositar es 1,000. ({monto:,.2f})")
            
            #monto maximo
            if monto > 3000000:
                raise ValueError(f"el monto maximo para depositar es 3,000,000. ({monto:,.2f})")
            
            #se realiza el deposito
            self.__saldo += monto
        except Exception as e:
            caja_negra.registrar_error("depositar dinero", e)
            raise

    def retirar(self, monto: float):
        try:
            #logica de validacion antes de efectuar el retiro
            #verificar que la cuenta este activa
            if self.__estado_cuenta != EstadoCuenta.ACTIVA.value:
                raise ValueError(f"el estado de la cuenta no permite permite retirar({self.__estado_cuenta})")
            
            #verificar que no sea un bool
            if isinstance(monto, bool):
                raise ValueError("el monto no puede ser booleano")
            
            #verificar que el monto sea numerico
            if not isinstance(monto, (int, float)):
                raise TypeError(f"el monto debe ser un valor numerico. ({monto})")
            
            #aplicando el estandar bancario y evitando los errores del float
            #se implementa la libreria Decimal
            monto = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            #monto mayor a 0
            if monto <= 0:
                raise ValueError(f"el monto debe ser mayor a 0({monto})")
            
            #monto minimo
            if monto < 1000:
                raise ValueError(f"el monto minimo para retirar es 1,000. ({monto:,.2f})")
            
            #monto maximo
            if monto > 3000000:
                raise ValueError(f"el monto maximo para retirar es 3,000,000. ({monto:,.2f})")

            #monto no supere el saldo
            if monto > self.__saldo:
                raise ValueError(f"saldo insuficiente. saldo actual:{self.__saldo:,.2f}, monto solicitado: {monto:,.2f}")

            #se realiza el retiro.
            self.__saldo -= monto
        except Exception as e:
            caja_negra.registrar_error("retirar dinero", e)
            raise
    
    def __str__(self):
        return f'Cuenta(ID: {self.__cuenta_id}, Numero: {self.__numero_cuenta}, Saldo: {self.__saldo:,.2f}, Estado: {self.__estado_cuenta})'
    
    @classmethod
    def cargar_cuenta_bd(cls, cuenta_id, saldo, numero_cuenta, fecha_creacion, cliente_id, estado_cuenta_id):

        #creamos una instancia "vacia" sin pasar por el __init__ convencional
        cuenta_existente = cls.__new__(cls)

        #se asigna automaticamente los valores a los atributos privados
        #saltandose los setters para no validar nada ya que los datos vienen de la BD

        cuenta_existente._Cuenta__cuenta_id = cuenta_id
        cuenta_existente._Cuenta__saldo = Decimal(str(saldo)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        cuenta_existente._Cuenta__numero_cuenta = numero_cuenta
        cuenta_existente._Cuenta__fecha_creacion = fecha_creacion
        cuenta_existente._Cuenta__cliente_id = cliente_id
        cuenta_existente._Cuenta__estado_cuenta = estado_cuenta_id

        return cuenta_existente