import re

class ResponseMessage:
    def __init__(self, Resultado=None, Exito=True, MensajePorFallo=""):
        self.Resultado = Resultado
        self.Exito = Exito
        self.MensajePorFallo = MensajePorFallo

    def obtenerResultado(self):
        return {
            "Resultado": self.Resultado,
            "Exito": self.Exito,
            "MensajePorFallo": self.MensajePorFallo
        }

class validaciones:
    def validar_estructura_email(email):
        # Definir la expresión regular para validar el email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Usar re.match para verificar si el email coincide con el patrón
        if re.match(patron, email):
            return True
        else:
            return False