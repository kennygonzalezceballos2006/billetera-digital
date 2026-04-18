import unittest
from modelos.cliente import Cliente
from modelos.catalogos.roles import Roles
from modelos.catalogos.estado_cliente import EstadoCliente
from modelos.catalogos.tipo_cliente import TipoCliente

class TestCliente(unittest.TestCase):

    def test_bloqueo_por_intentos(self):
        # Preparación (Arrange)
        user = Cliente("test@mail.com", "Clave123*", Roles.CLIENTE, EstadoCliente.ACTIVO, TipoCliente.PERSONA_NATURAL)
        
        # Acción (Act)
        user.verificar_credenciales("test@mail.com", "error1")
        user.verificar_credenciales("test@mail.com", "error2")
        user.verificar_credenciales("test@mail.com", "error3")
        
        # Verificación (Assert)
        # Esto es lo que lo hace un Unit Test: el framework verifica el resultado
        self.assertEqual(user.estado_cliente_id, EstadoCliente.BLOQUEADO.value)

if __name__ == '__main__':
    unittest.main()