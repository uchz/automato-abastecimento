
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pywhatkit as kit

# CONFIG
URL = "http://10.10.2.2:8080/webservice_mfc/tratativaPickingKingOuro.html"
NUMERO = "+5521969932512"  # ex: +5511999999999

itens_vistos = set()

driver = webdriver.Chrome()
driver.get(URL)

time.sleep(10)  # tempo pra carregar / login manual

def enviar_whatsapp(msg):
    # envia instantâneo (abre aba)
    kit.sendwhatmsg_instantly(NUMERO, msg, wait_time=10, tab_close=True)

while True:
    try:
        linhas = driver.find_elements(By.XPATH, "//table//tbody/tr")

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")

            data = colunas[0].text
            endereco = colunas[2].text
            cod_produto = colunas[7].text
            descricao = colunas[8].text

            chave = f"{cod_produto}-{endereco}"

            if chave not in itens_vistos:
                itens_vistos.add(chave)

                msg = (
                    f"🚨 ITEM FALTANTE NOVO\n"
                    f"Produto: {cod_produto}\n"
                    f"Endereço: {endereco}\n"
                    f"Hora: {data}"
                )


                print(msg)
                enviar_whatsapp(msg)
                

        time.sleep(30)  # verifica a cada 30s

    except Exception as e:
        print("Erro:", e)
        time.sleep(10)
# %%
