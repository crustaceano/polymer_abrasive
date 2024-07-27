from dotenv import load_dotenv
import os
load_dotenv()

# Получение значений переменных
SMTP_SERVER = os.getenv('SMTP_SERVER', "smtp.mail.ru")
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USER = os.getenv('SMTP_USER', "example@mail.ru")
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'some_password')