import threading
import time
import urllib.parse
from queue import Queue

import customtkinter as ctk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# CONFIG
URL = "http://10.10.2.2:8080/webservice_mfc/tratativaPickingKingOuro.html"

# ==============================
# CONTROLE GLOBAL
# ==============================

log_queue = Queue()
rodando = False

def log(msg):
    log_queue.put(msg)

# ==============================
# BOT
# ==============================

def iniciar_bot(numero, nome_grupo):
    global rodando

    itens_vistos = set()
    contador = 0

    options = Options()
    options.add_argument(r"user-data-dir=C:\selenium_profile")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    time.sleep(10)

    log("🚀 Bot iniciado")

    def enviar_whatsapp(msg):
        try:
            msg_formatada = urllib.parse.quote(msg)

            url = f"https://web.whatsapp.com/send?phone={numero}&text={msg_formatada}"
            driver.get(url)

            time.sleep(15)

            botao = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[4]/div/span')
            botao.click()

            time.sleep(5)
            driver.get(URL)

        except Exception as e:
            log(f"Erro WhatsApp: {e}")
            driver.get(URL)

    while rodando:
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

            for msg in novos_itens:
                log(msg)
                enviar_whatsapp(msg)
                contador_label.configure(text=f"Ocorrências: {contador}")
                time.sleep(2)

            time.sleep(15)

        except Exception as e:
            log(f"Erro geral: {e}")
            time.sleep(5)

    driver.quit()
    log("🛑 Bot parado")

# ==============================
# INTERFACE
# ==============================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Monitor de Ocorrências")
app.geometry("400x500")

# título
titulo = ctk.CTkLabel(app, text="🚨 Monitor de Ocorrências", font=("Arial", 18))
titulo.pack(pady=10)

# status
status_label = ctk.CTkLabel(app, text="Status: 🔴 Parado")
status_label.pack()

# contador
contador_label = ctk.CTkLabel(app, text="Ocorrências: 0")
contador_label.pack(pady=5)

# entrada telefone
entry_numero = ctk.CTkEntry(app, placeholder_text="55 + DDD + Número")
entry_numero.insert(0, "55")
entry_numero.pack(pady=10)

# entrada grupo
entry_grupo = ctk.CTkEntry(app, placeholder_text="Grupo (opcional)")
entry_grupo.pack(pady=5)

# ==============================
# BOTÕES
# ==============================

def iniciar():
    global rodando

    numero = entry_numero.get()
    grupo = entry_grupo.get()

    if not numero.startswith("55"):
        numero = "55" + numero

    if not numero.isdigit():
        messagebox.showerror("Erro", "Número inválido!")
        return

    if rodando:
        return

    rodando = True

    status_label.configure(text="Status: 🟢 Rodando")
    log("Iniciando bot...")

    thread = threading.Thread(target=iniciar_bot, args=(numero, grupo))
    thread.daemon = True
    thread.start()

def parar():
    global rodando
    rodando = False
    status_label.configure(text="Status: 🔴 Parado")
    log("Parando bot...")

# botões
frame_botoes = ctk.CTkFrame(app)
frame_botoes.pack(pady=10)

btn_iniciar = ctk.CTkButton(frame_botoes, text="Iniciar", command=iniciar)
btn_iniciar.pack(side="left", padx=10)

btn_parar = ctk.CTkButton(frame_botoes, text="Parar", command=parar)
btn_parar.pack(side="left", padx=10)

# ==============================
# LOG
# ==============================

log_box = ctk.CTkTextbox(app, width=350, height=250)
log_box.pack(pady=10)

def atualizar_log():
    while not log_queue.empty():
        msg = log_queue.get()

        log_box.configure(state="normal")
        log_box.insert("end", msg + "\n")
        log_box.configure(state="disabled")
        log_box.see("end")

    app.after(500, atualizar_log)

atualizar_log()

app.mainloop()