#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse

# CONFIG
URL = "http://10.10.2.2:8080/webservice_mfc/tratativaPickingKingOuro.html"
NUMERO = "5521975372117"  # sem o +
NOME_GRUPO = 'Faltas Picking'

# salva sessão do WhatsApp
options = Options()
options.add_argument(r"user-data-dir=C:\selenium_profile")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=options)

driver.get(URL)

time.sleep(14)  # tempo pra login manual

itens_vistos = set()
#%%
# def abrir_whatsapp():
#     driver.get("https://web.whatsapp.com/")
#     time.sleep(17)

# def enviar_grupo(msg):
#     try:
        
#         abrir_whatsapp()
#         # caixa de busca (primeira que aparece)
#         busca = driver.find_element(By.XPATH,'//*[@id="_r_a_"]')
#         busca.click()
#         time.sleep(2)

#         busca.clear()
#         busca.send_keys(NOME_GRUPO)
#         time.sleep(3)

#         # clicar no grupo
#         grupo = driver.find_element(By.XPATH, f"//span[@title='{NOME_GRUPO}']")
#         grupo.click()
#         time.sleep(2)

#         # caixa de mensagem (última caixa editável)
#         caixa_msg = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[3]/div[1]/p')
        

#         caixa_msg.click()
#         caixa_msg.send_keys(msg)
#         time.sleep(2)

#         # botão enviar
#         botao = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[4]/div/span/button')
#         botao.click()

#         time.sleep(3)

#         # volta pro sistema
#         driver.get(URL)
#         time.sleep(3)

#     except Exception as e:
#         print("Erro ao enviar para grupo:", e)
#         driver.get(URL)

def enviar_whatsapp(msg):
    try:
        msg_formatada = urllib.parse.quote(msg)

        url = f"https://web.whatsapp.com/send?phone={NUMERO}&text={msg_formatada}"
        driver.get(url)

        time.sleep(15)

        botao = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[4]/div/span')
        botao.click()

        time.sleep(2)

        # volta pro sistema
        driver.get(URL)
        time.sleep(3)

    except Exception as e:
        print("Erro ao enviar WhatsApp:", e)
        driver.get(URL)

print("🚀 Monitorando itens faltantes...")


#%% 
contador = 0

while True:
    try:
        linhas = driver.find_elements(By.XPATH, "//table//tbody/tr")

        novos_itens = []

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")

            if len(colunas) < 9:
                continue

            data = colunas[0].text
            endereco = colunas[2].text
            cod_produto = colunas[7].text


            chave = f"{cod_produto}-{endereco}"

            if chave not in itens_vistos:
                itens_vistos.add(chave)

                contador += 1

                msg = (
                    f"🚨 Ocorrência #{contador}\n\n"
                    f"Produto: {cod_produto}\n"
                    f"Endereço: {endereco}\n"
                    f"Hora: {data}"
                )

                novos_itens.append(msg)

        # 👇 AGORA envia depois de coletar tudo
        for msg in novos_itens:
            print(msg)
            enviar_whatsapp(msg)

        time.sleep(15)

    except Exception as e:
        print("Erro geral:", e)
        time.sleep(3)

# %%
