import requests
import email.message
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def info_kabum(url, headers, session):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {url} - {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h1', {'class': 'sc-58b2114e-6 brTtKt'})
    price_element = soup.find('b', {'class': 'regularPrice'})

    if title_element and price_element:
        price = price_element.text.strip().replace("\xa0", "")
        title = title_element.text.strip().split(',')[0]
        return price, title
    else:
        price_element = soup.find('h4', {'class': 'sc-5492faee-2 ipHrwP finalPrice'})
        if title_element and price_element:
            price = price_element.text.strip().replace("\xa0", "")
            title = title_element.text.strip().split(',')[0]
            return price, title
        else:
            return None

def info_nba(url, headers, session):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {url} - {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h1', {'class': 'product-name'})
    price_container = soup.find('p', {'class': 'payment-method-communication'})
    
    if title_element and price_container:
        span_price = price_container.find('span')
        if span_price:
            price = span_price.text.strip().replace("ou", "").split('em')[0].replace(" ", "")
            title = title_element.text.strip().split(',')[0]
            return price, title

def send_email():
    server_smtp = "smtp.gmail.com"
    port = 587
    sender_email = ""
    password = ""
    receive_email = ""
    subject = "teste_email"
    body = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Teste</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f2f2f2;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f2f2f2;">
        <tr>
            <td align="center">
                <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff;">
                    <tr>
                        <td align="center" style="padding: 40px 0;">
                            <img src="https://img.freepik.com/fotos-gratis/paisagem-de-nevoeiro-matinal-e-montanhas-com-baloes-de-ar-quente-ao-nascer-do-sol_335224-794.jpg" alt="Paisagem" width="400" style="display: block; margin: 0 auto;">
                            <p style="margin-top: 20px; text-align: center;">Olá,</p>
                            <p style="text-align: center;">Este é um e-mail de teste com uma imagem anexada.</p>
                            <p style="text-align: center;">Agradecemos por ter recebido este e-mail de teste.</p>
                            <p style="text-align: center;">Este e-mail foi enviado apenas para fins de demonstração e teste.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
    message = MIMEMultipart()
    message["From"] = sender_email
    message ["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
        print("email enviado com sucesso")
    finally:
        server.quit()
