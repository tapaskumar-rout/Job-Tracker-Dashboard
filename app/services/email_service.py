from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.mail import conf

class EmailService:

  @staticmethod
  async def send_reset_email(email: str, reset_link:str):

    message = MessageSchema(
      subject="Reset Your Job Tracker Password",
      recipients=[email],
      body=f"""
      <h2>Password Reset</h2>

      <p>Click the link below to reset your password:</p>

      <a href="{reset_link}">
       Reset Password
            </a>

            <br><br>

            <p>If you didn't request this, you can ignore this email.</p>
            """,
            subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
