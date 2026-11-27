"""
Cron job runs this to send email
"""
import asyncio
import logging

from app.database import Base, engine
from app.services.digest import generate_digest
from app.services.email import send_email

logging.basicConfig(level=logging.INFO)


async def main():
    # Ensure database and tables exist
    Base.metadata.create_all(bind=engine)

    print("Generating digest...")
    html = await generate_digest()

    print("Sending email...")
    send_email(
        subject="Morning Digest ☀️",
        html_content=html,
    )
    print("Digest email sent successfully!")


if __name__ == "__main__":
    asyncio.run(main())