import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

def send_email_with_attachment(to_email: str, subject: str, body: str, attachment_path: Path):
    """
    SMTP credentials must be set via environment variables:
      SMTP_HOST (e.g., smtp.gmail.com)
      SMTP_PORT (e.g., 587)
      SMTP_USER (your email)
      SMTP_PASS (app password / smtp password)
      FROM_EMAIL (optional; defaults to SMTP_USER)
    """
    host = os.environ.get("SMTP_HOST", "").strip()
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "").strip()
    pw = os.environ.get("SMTP_PASS", "").strip()
    from_email = os.environ.get("FROM_EMAIL", user).strip()

    if not (host and user and pw and from_email):
        raise RuntimeError("SMTP env vars missing. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL.")

    attachment_path = Path(attachment_path)
    if not attachment_path.exists():
        raise FileNotFoundError(f"Attachment not found: {attachment_path}")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    data = attachment_path.read_bytes()
    msg.add_attachment(data, maintype="application", subtype="zip", filename=attachment_path.name)

    with smtplib.SMTP(host, port) as s:
        s.ehlo()
        s.starttls()
        s.login(user, pw)
        s.send_message(msg)
