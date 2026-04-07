"""
Helper seguro para envío de correos (wrapper):
- No envía nada si no configuras variables de entorno SMTP
- Uso: from mail import send_email; send_email(destinatario, asunto, cuerpo)
"""
import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587)) if os.environ.get('SMTP_PORT') else None
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USER)


def send_email(to_address, subject, body, html=False):
    """Envía un email si hay configuración SMTP. Devuelve True si se envió, False si no se intentó.
    """
    if not SMTP_HOST or not SMTP_PORT or not SMTP_USER or not SMTP_PASS:
        # No hay configuración SMTP, no intentamos enviar — útil para deploys sin credenciales
        print("mail.py: SMTP no configurado. Email no enviado.")
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_address
    if html:
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"mail.py: Error enviando email: {e}")
        return False
