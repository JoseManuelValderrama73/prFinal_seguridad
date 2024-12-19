import smtplib
from email.mime.text import MIMEText
import random
import string


def enviar_correo(destinatario, asunto, mensaje):
    servidor = "smtp.gmail.com"
    puerto = 587
    remitente = "gestorcontrasena2024@gmail.com"
    contrasena = "zbjr apqq lsew ravm"

    msg = MIMEText(mensaje)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP(servidor, puerto) as server:
            server.starttls()
            server.login(remitente, contrasena)
            server.sendmail(remitente, destinatario, msg.as_string())
    except Exception as e:
        print(f"Error al enviar correo: {e}")


def generar_codigo_recuperacion():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def recuperar_clave(destinatario):
    codigo = generar_codigo_recuperacion()

    enviar_correo(
        destinatario,
        "Recuperacion de la clave maestra",
        f"Tu código de recuperación es: {codigo}",
    )
    return codigo
