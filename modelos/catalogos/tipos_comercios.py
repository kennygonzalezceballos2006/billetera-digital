from enum import Enum

class TipoComercio(Enum):
    # Alimentación
    TIENDA = 1
    RESTAURANTE = 2
    FRUVER = 3
    PANADERIA = 4
    CARNICERIA = 5
    PESCADERIA = 6
    CAFETERIA = 7
    HELADERIA = 8
    CEVICHERIA = 9
    COMIDAS_RAPIDAS = 10

    # Salud y belleza
    FARMACIA = 11
    DROGUERIA = 12
    PELUQUERIA = 13
    BARBERIA = 14
    SPA = 15
    OPTICA = 16

    # Hogar y construcción
    FERRETERIA = 17
    CERAMICAS = 18
    DEPOSITO_MATERIALES = 19
    MUEBLERIA = 20
    ELECTRICOS = 21

    # Tecnología
    TECNICEL = 22
    ACCESORIOS_CELULAR = 23
    SERVICIO_TECNICO = 24
    INTERNET_CAFE = 25

    # Educación y papelería
    PAPELERIA = 26
    LIBRERIA = 27
    FOTOCOPIAS = 28

    # Ropa y calzado
    ROPA = 29
    CALZADO = 30
    ACCESORIOS_MODA = 31

    # Transporte
    MOTOTAXI = 32
    LAVADERO = 33
    TALLER_MECANICO = 34
    VENTA_REPUESTOS = 35

    # Entretenimiento
    BILLAR = 36
    VIDEOjuegos = 37
    ESTADERO = 38
    BAR = 39

    # Servicios varios
    MISCELANEA = 40
    SASTRE = 41
    ZAPATERO = 42
    CERRAJERIA = 43
    LAVANDERIA = 44
    SERVICIO_GAS = 45
    VENTA_MINUTOS = 46
    CHANCE = 47

    # Típico La Guajira
    ARTESANIAS = 48
    VENTA_CHIVO = 49
    VENTA_PESCADO_SECO = 50
    VENTA_CARBON = 51
    VENTA_LEÑA = 52
    CHINCHORRO = 53