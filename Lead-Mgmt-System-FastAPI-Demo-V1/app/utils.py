# utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to: str, subject: str, body: str):
    try:
        sender_email = "your@email.com"
        receiver_email = to
        password = "your-email-password"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)
    except Exception as e:
        print("SMTP server is not setup hence can not send emails")
        print(e.__traceback__)
    finally:
        server.quit()
    