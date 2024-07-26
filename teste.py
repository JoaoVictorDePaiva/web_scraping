import requests
import functions
import email.message
import smtplib
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
Urls_Kabum = [
    "https://www.kabum.com.br/produto/102770/headset-gamer-havit-drivers-53mm-microfone-plugavel-p2-pc-ps4-xbox-one-preto-hv-h2002d",
    "https://www.kabum.com.br/produto/94555/mouse-gamer-redragon-cobra-chroma-rgb-10000dpi-7-botoes-preto-m711-v2",
    "https://www.kabum.com.br/produto/362905/cabo-dados-sata-3-ugreen-6gbps-hd-ssd-gravador-gamer-50cm",
    "https://www.kabum.com.br/produto/386758/hd-interno-western-digital-2tb-blue-5400-rpm-256mb-3-5-sata-iii-20ezaz"
]

Urls_nba = ["https://www.lojanba.com/p/tenis-nba-nike-giannis-immortality-3-masculino-preto+branco-JD8-3946-028"]

header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

produtos = []
precos = []

session = requests.Session()
retry = Retry(connect=10, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

for url in Urls_Kabum:
    teste1 = functions.info_kabum(url, header, session)
    if teste1:  # Verifica se a função retornou algo válido
        price, title = teste1  # Desempacota a tupla
        precos.append(price)
        produtos.append(title)

for url in Urls_nba:
    teste2 = functions.info_nba(url, header, session)
    if teste2: 
        price, title = teste2 
        precos.append(price)
        produtos.append(title)


print(produtos)
print(precos)
functions.send_email()
