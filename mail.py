"""Helper mínimo para enviar correos de forma opcional.

Si no están definidas las variables de entorno SMTP_* o FROM_EMAIL, las funciones
no hacen nada y devuelven False (no fallan), evitando ImportError o fallos en runtime.

Uso recomendado desde la app:
    from mail import send_mail
    send_mail(to, subject, body)

No hace llamadas externas si las credenciales faltan.
"""
from typing import List, Optional
import os
import smtplib
from email.message import EmailMessage


def _smtp_config_present() -> bool:
    return bool(os.environ.get('SMTP_HOST') and os.environ.get('SMTP_USER') and os.environ.get('SMTP_PASS') and os.environ.get('FROM_EMAIL'))


def send_mail(to: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> bool:
    """Enviar correo sencillo.

    Si no hay configuración SMTP en variables de entorno, la función hace noop y devuelve False.
    Devuelve True si el envío fue intentado con la configuración encontrada.
    """
    if not _smtp_config_present():
        # No SMTP configured — noop
        return False

    host = os.environ.get('SMTP_HOST')
    port = int(os.environ.get('SMTP_PORT') or 587)
    user = os.environ.get('SMTP_USER')
    password = os.environ.get('SMTP_PASS')
    from_email = os.environ.get('FROM_EMAIL')

    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach files if provided
    if attachments:
        for path in attachments:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                import mimetypes
                ctype, encoding = mimetypes.guess_type(path)
                if ctype is None:
                    maintype, subtype = 'application', 'octet-stream'
                else:
                    maintype, subtype = ctype.split('/', 1)
                msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(path))
            except Exception:
                # Ignore attachment errors — keep sending the rest
                continue

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
        return True
    except Exception:
        return False
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
