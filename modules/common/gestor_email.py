from modules.common.gestor_comun import ResponseMessage, validaciones
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

class gestor_email(ResponseMessage):
    def __init__(self):
        super().__init__()
                
    def enviar_email(self,recipient_email, subject, body):

        if not validaciones.validar_estructura_email(recipient_email):
            self.Exito = False
            self.MensajePorFallo = "El email tiene una estructura no válida."
            return False
        
        # Configuración del servidor de correo
        smtp_server = "smtp.gmail.com"  # Cambia si se usa otro proveedor de correo
        smtp_port = 587  # Puerto SMTP
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")

        # Crear objeto MIMEMultipart para el mensaje
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Agregar el cuerpo del mensaje
        msg.attach(MIMEText(body, 'plain'))

        # Agregar una copia del correo a la dirección de origen
        msg.add_header('Cc', sender_email)

        # Iniciar la conexión al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        try:
            # Iniciar sesión en la cuenta de correo
            server.login(sender_email, sender_password)
            
            # Enviar el mensaje
            server.sendmail(sender_email, [recipient_email, sender_email], msg.as_string())
            return self.obtenerResultado()
        except Exception as e:
            self.Exito = False
            self.MensajePorFallo = f"Error al enviar el email: {e}"
            return False
        finally:
            # Cerrar la conexión
            server.quit()