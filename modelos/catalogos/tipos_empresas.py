from enum import Enum

class TipoEmpresa(Enum):
    #sociedades comerciales
    SOCIEDAD_ANONIMA_SIMPLIFICADA = 1        # SAS — la más común en Colombia
    SOCIEDAD_ANONIMA = 2                      # SA
    SOCIEDAD_LIMITADA = 3                     # LTDA
    SOCIEDAD_COLECTIVA = 4
    SOCIEDAD_EN_COMANDITA_SIMPLE = 5
    SOCIEDAD_EN_COMANDITA_POR_ACCIONES = 6

    # Unipersonal
    EMPRESA_UNIPERSONAL = 7
    PERSONA_NATURAL_COMERCIANTE = 8

    # Sin ánimo de lucro
    FUNDACION = 9
    ASOCIACION = 10
    CORPORACION = 11
    COOPERATIVA = 12
    FONDO_COMUNITARIO = 13

    # Sector público
    EMPRESA_INDUSTRIAL_COMERCIAL_ESTADO = 14  # EICE
    SOCIEDAD_ECONOMIA_MIXTA = 15

    # Sector financiero
    BANCO = 16
    COOPERATIVA_FINANCIERA = 17
    COMPANIA_SEGUROS = 18

    # Otros
    CONSORCIO = 19
    UNION_TEMPORAL = 20