from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="quantumcode.team@gmail.com",
    MAIL_PASSWORD="pqml sfzh cqum vkmj",
    MAIL_FROM="quantumcode.team@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_verification_code(email, code):
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=f"Your verification code is {code}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
