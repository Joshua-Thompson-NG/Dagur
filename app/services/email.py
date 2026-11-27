import logging
import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)
EMAIL_TO = os.getenv("EMAIL_TO", "")


def send_email(
    subject: str,
    html_content: str,
    text_content: str | None = None,
    recipient: str | None = None,
) -> bool:
    """
    Sends an email using SMTP with both plain-text and HTML formatting.

    Args:
        subject: Subject line of the email.
        html_content: HTML body for formatted email clients.
        text_content: Fallback plain-text body for simple clients.
        recipient: Optional override recipient address (defaults to EMAIL_TO env var).

    Returns:
        True if the email was sent successfully, False otherwise.
    """
    to_email = recipient or EMAIL_TO
    from_email = EMAIL_FROM or SMTP_USER

    if not to_email:
        logger.error("No recipient email specified (EMAIL_TO is not set).")
        raise ValueError("Recipient email is required.")

    if not SMTP_USER or not SMTP_PASSWORD:
        logger.error("SMTP credentials (SMTP_USER / SMTP_PASSWORD) are not configured.")
        raise ValueError("SMTP credentials are not configured.")

    # Build the multipart email message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    # Plain-text fallback
    if text_content:
        msg.set_content(text_content)
    else:
        # Default plain-text if only HTML provided
        msg.set_content("Please view this email with an HTML-compatible email client.")

    # Add HTML version as an alternative
    msg.add_alternative(html_content, subtype="html")

    # Connect to SMTP server and deliver
    try:
        if SMTP_PORT == 465:
            # SSL connection
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            # STARTTLS connection (standard for port 587)
            context = ssl.create_default_context()
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as auth_err:
        logger.error(f"SMTP authentication failed: {auth_err}")
        raise
    except smtplib.SMTPException as smtp_err:
        logger.error(f"SMTP error occurred while sending email: {smtp_err}")
        raise
    except Exception as exc:
        logger.error(f"Unexpected error while sending email: {exc}")
        raise
