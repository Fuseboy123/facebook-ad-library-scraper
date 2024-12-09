import requests
import time
from bs4 import BeautifulSoup

# Configuração do Telegram
BOT_TOKEN = '7866607840:AAFRdr1e7LwuUnUZ2mFXG1XWSXxCPV62rnQ'
CHAT_ID = '1725903374'

# Função para criar o termômetro baseado em porcentagem
def termometro_emojis(percent):
    if percent <= 20:
        return "\ud83d\ude21"  # Muito ruim
    elif percent <= 40:
        return "\ud83d\ude41"  # Ruim
    elif percent <= 60:
        return "\ud83d\ude10"  # Neutro
    elif percent <= 80:
        return "\ud83d\ude42"  # Bom
    else:
        return "\ud83d\ude04"  # Excelente

# Função para enviar mensagens formatadas ao Telegram
def send_to_telegram(nome, bonus, termometro, link):
    # Aplicando cores ao bônus
    if bonus.lower() == "sem informa\u00e7\u00f5es":
        bonus = f"<b><span style=\"color:orange;\">{bonus}</span></b>"
    else:
        bonus = f"<b><span style=\"color:green;\">{bonus}</span></b>"

    # Formatação da mensagem
    message = (
        f"<b>\u2b50 Nome da Bet:</b> <i>{nome}</i>\n"
        f"<b>\ud83c\udf81 Bônus:</b> {bonus}\n"
        f"<b>\ud83c\udf21\ufe0f Termômetro:</b> {termometro_emojis(termometro)} ({termometro}%)\n"
        f"<b><a href=\"{link}\">\ud83d\udd17 Link</a></b>"
    )

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.json()

# Função de scraping (substitua com o código do facebook-ad-library-scraper)
def scrape_ads():
    ads = []
    # Exemplo de scraping simples - ajuste para o site de onde coletará os dados
    url = "https://www.facebook.com/ads/library/?active_status=all"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Substitua pelos seletores reais do site para coletar dados
    for ad in soup.select('.ad-class-selector')[:5]:  # Ajuste o seletor CSS
        nome = ad.select_one('.nome-class').text.strip() if ad.select_one('.nome-class') else "N/A"
        bonus = ad.select_one('.bonus-class').text.strip() if ad.select_one('.bonus-class') else "Sem informa\u00e7\u00f5es"
        termometro = ad.select_one('.termometro-class').text.strip() if ad.select_one('.termometro-class') else "0"
        link = ad.select_one('a')['href'] if ad.select_one('a') else "N/A"
        ads.append((nome, bonus, int(termometro), link))
    return ads

# Loop para executar o scraping e enviar os anúncios de hora em hora
while True:
    print("Iniciando o scraping...")
    try:
        ads = scrape_ads()
        for nome, bonus, termometro, link in ads:
            send_to_telegram(nome, bonus, termometro, link)
        print("Anúncios enviados com sucesso!")
    except Exception as e:
        print(f"Erro durante o processo: {e}")
    print("Aguardando 1 hora...")
    time.sleep(3600)  # Espera 1 hora antes da próxima execução
