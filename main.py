from fastapi import FastAPI, Form
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


class Order(BaseModel):
    name: str
    email: EmailStr
    phone: str
    details: str


@app.post("/order")
async def submit_order(
        name: str = Form(...),
        email: EmailStr = Form(...),
        phone: str = Form(...),
        details: str = Form(...),
):
    order = Order(name=name, email=email, phone=phone, details=details)
    await send_email(order)
    return {"message": "Заказ успешно отправлен"}


async def send_email(order: Order):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER
    msg["Subject"] = "Новый заказ"

    body = f"""
    Имя: {order.name}
    Email: {order.email}
    Телефон: {order.phone}
    Детали заказа: {order.details}
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
        )
    except Exception as e:
        print(f"Error sending email: {e}")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
