class PersonaNatural:
    def __init__(self, nombres, apellidos, telefono, documento_identificacion, fecha_nacimiento, cliente_id: int = None):
        self.__cliente_id = cliente_id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.documento_identificacion = documento_identificacion
        self.fecha_nacimiento = fecha_nacimiento
    
    #Getters para acceder mediante un metodo que actua como atributo
    #lee el valor del atributo y lo retorna
    @property
    def cliente_id(self):
        return self.__cliente_id

    @property
    def nombres(self):
        return self.__nombres
    
    @property
    def apellidos(self):
        return self.__apellidos
    
    @property
    def telefono(self):
        return self.__telefono
    
    @property
    def documento_identificacion(self):
        return self.__documento_identidicacion
    
    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento
    
    #Setters para acceder y modificar el valor de un atributo privado mediante una logica de validacion
    #actua tanto para modificar como para insertar un valor a un atributo de una nueva instancia(PeronaNatural)
    