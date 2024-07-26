import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

URLS = [
    "https://www.kabum.com.br/produto/102770/headset-gamer-havit-drivers-53mm-microfone-plugavel-p2-pc-ps4-xbox-one-preto-hv-h2002d",
    "https://www.kabum.com.br/produto/94555/mouse-gamer-redragon-cobra-chroma-rgb-10000dpi-7-botoes-preto-m711-v2",
    "https://www.kabum.com.br/produto/362905/cabo-dados-sata-3-ugreen-6gbps-hd-ssd-gravador-gamer-50cm",
    "https://www.kabum.com.br/produto/386758/hd-interno-western-digital-2tb-blue-5400-rpm-256mb-3-5-sata-iii-20ezaz"
]

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

produtos = []
precos = []

session = requests.Session()
retry = Retry(connect=10, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def info_kabum(url, headers, session):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {url} - {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h1', {'class': 'sc-58b2114e-6 brTtKt'})
    price_element = soup.find('b', {'class': 'regularPrice'})

    if title_element and price_element:
        price = price_element.text.strip().replace("\xa0", "")
        title = title_element.text.strip().split(',')[0]
    else:
        price_element = soup.find('h4', {'class': 'sc-5492faee-2 ipHrwP finalPrice'})
        if title_element and price_element:
            price = price_element.text.strip().replace("\xa0", "")
            title = title_element.text.strip().split(',')[0]
        else:
            print(f"Erro ao encontrar título ou preço para a URL: {url}")
            return

    produtos.append(title)
    precos.append(price)

for url in URLS:
    info_kabum(url, headers, session)

print(produtos)
print(precos)