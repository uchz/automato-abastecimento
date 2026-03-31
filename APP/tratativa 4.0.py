import threading
import time
import urllib.parse
from queue import Queue
import requests

import customtkinter as ctk
from tkinter import messagebox
import csv
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import ttk

# ==============================
# CONFIG
# ==============================
URL = "http://10.10.2.2:8080/webservice_mfc/tratativaPickingKingOuro.html"

# ==============================
# CONTROLE GLOBAL
# ==============================
log_queue = Queue()
fila_envio = Queue()
ui_queue = Queue()

rodando = False
ultimo_evento = datetime.now()
tempo_alerta_minutos = 5
alerta_disparado = False

# ==============================
# LOG
# ==============================
def log(msg):
    horario = datetime.now().strftime("%H:%M:%S")
    log_queue.put(f"[{horario}] {msg}")

# ==============================
# CSV
# ==============================
def salvar_csv(data, produto, endereco):
    arquivo = "historico_ocorrencias.csv"
    arquivo_existe = os.path.isfile(arquivo)

    with open(arquivo, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        if not arquivo_existe:
            writer.writerow(["Data", "Produto", "Endereço", "Hora", "Timestamp"])

        agora = datetime.now()

        writer.writerow([
            data,
            produto,
            endereco,
            agora.strftime("%H:%M:%S"),
            agora.strftime("%Y-%m-%d %H:%M:%S")
        ])

# ==============================
# BOT
# ==============================
def iniciar_bot(numero):
    global rodando, ultimo_evento, alerta_disparado

    itens_vistos = set()
    contador = 0

    options = Options()
    options.add_argument(r"user-data-dir=C:\selenium_profile_monitor")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    options_wpp = Options()
    options_wpp.add_argument(r"user-data-dir=C:\selenium_profile_wpp")
    driver_wpp = webdriver.Chrome(options=options_wpp)
    driver_wpp.get("https://web.whatsapp.com")

    log("🚀 Bot iniciado")

    def worker_whatsapp():
        while rodando:
            try:
                if fila_envio.qsize() > 10:
                    log("⚠ Muitas mensagens acumuladas...")
                    time.sleep(10)

                msg = fila_envio.get()

                msg_formatada = urllib.parse.quote(msg)
                url = f"https://web.whatsapp.com/send?phone={numero}&text={msg_formatada}"

                driver_wpp.get(url)

                WebDriverWait(driver_wpp, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer'))
                )

                botao = driver_wpp.find_element(
                    By.XPATH,
                    '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[4]/div/span'
                )
                botao.click()

                log("📤 Mensagem enviada")
                time.sleep(5)
                fila_envio.task_done()

            except Exception as e:
                log(f"❌ WhatsApp: {e}")

    threading.Thread(target=worker_whatsapp, daemon=True).start()

    while rodando:
        try:
            linhas = driver.find_elements(By.XPATH, "//table//tbody/tr")

            for linha in linhas:
                if not rodando:
                    break

                try:
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

                        salvar_csv(data, cod_produto, endereco)

                        msg = (
                            f"🚨 Ocorrência #{contador}\n"
                            f"Produto: {cod_produto}\n"
                            f"Endereço: {endereco}\n"
                            f"Hora: {data}"
                        )
                        requests.post(
                            "http://127.0.0.1:8000/ocorrencias",
                            json={
                                "produto": cod_produto,
                                "endereco": endereco,
                                "data": data
                            }
                        )

                        log(msg)
                        fila_envio.put(msg)

                        # atualiza contador via UI thread
                        ui_queue.put(("contador", contador))

                        # atualiza tempo de atividade
                        ultimo_evento = datetime.now()
                        alerta_disparado = False

                except StaleElementReferenceException:
                    continue

            time.sleep(10)

        except Exception as e:
            log(f"❌ Erro geral: {e}")
            time.sleep(5)

    driver.quit()
    driver_wpp.quit()
    log("🛑 Bot parado")




# ==============================
# ALERTA INATIVIDADE
# ==============================
def verificar_inatividade():
    global alerta_disparado

    agora = datetime.now()
    diff = (agora - ultimo_evento).total_seconds() / 60

    if diff >= tempo_alerta_minutos and not alerta_disparado:
        log(f"⚠ ALERTA: Sem ocorrências há {int(diff)} minutos!")
        alerta_disparado = True

    app.after(60000, verificar_inatividade)

# ==============================
# UI
# ==============================
def iniciar():
    global rodando

    numero = entry_numero.get()

    if not numero.startswith("55"):
        numero = "55" + numero

    if not numero.isdigit():
        messagebox.showerror("Erro", "Número inválido!")
        return

    if rodando:
        return

    rodando = True

    btn_iniciar.configure(state="disabled")
    btn_parar.configure(state="normal")

    status_label.configure(text="🟢 Rodando", text_color="green")
    log("Iniciando bot...")

    thread = threading.Thread(target=iniciar_bot, args=(numero,))
    thread.daemon = True
    thread.start()


def parar():
    global rodando
    rodando = False

    btn_iniciar.configure(state="normal")
    btn_parar.configure(state="disabled")

    status_label.configure(text="🔴 Parado", text_color="red")
    log("Parando bot...")

# ==============================
# INTERFACE
# ==============================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Painel de Ocorrências PRO")
app.geometry("700x550")

tabview = ctk.CTkTabview(app)
tabview.pack(expand=True, fill="both", padx=10, pady=10)

aba_monitor = tabview.add("Monitor")
aba_historico = tabview.add("Histórico")

container = ctk.CTkFrame(aba_monitor, corner_radius=15)
container.pack(expand=True, fill="both", padx=10, pady=10)

container.grid_rowconfigure(4, weight=1)
container.grid_columnconfigure(0, weight=1)

titulo = ctk.CTkLabel(container, text="🚨 Painel de Ocorrências", font=("Arial", 20, "bold"))
titulo.grid(row=0, column=0, pady=(15, 5))

frame_cards = ctk.CTkFrame(container, fg_color="transparent")
frame_cards.grid(row=1, column=0, pady=5)

status_label = ctk.CTkLabel(frame_cards, text="🔴 Parado", font=("Arial", 14, "bold"))
status_label.pack(side="left", padx=20)

contador_label = ctk.CTkLabel(frame_cards, text="Ocorrências: 0", font=("Arial", 14))
contador_label.pack(side="left", padx=20)

entry_numero = ctk.CTkEntry(container, placeholder_text="55 + DDD + Número", width=250)
entry_numero.insert(0, "55")
entry_numero.grid(row=2, column=0, pady=10)

frame_botoes = ctk.CTkFrame(container, fg_color="transparent")
frame_botoes.grid(row=3, column=0, pady=10)

btn_iniciar = ctk.CTkButton(frame_botoes, text="▶ Iniciar", width=120, command=iniciar)
btn_iniciar.pack(side="left", padx=10)

btn_parar = ctk.CTkButton(frame_botoes, text="⏹ Parar", width=120, command=parar)
btn_parar.pack(side="left", padx=10)
btn_parar.configure(state="disabled")

log_box = ctk.CTkTextbox(container, corner_radius=10)
log_box.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

# ==============================
# HISTÓRICO
# ==============================
colunas = ("Data", "Produto", "Endereço", "Hora", "Timestamp")

tabela = ttk.Treeview(aba_historico, columns=colunas, show="headings")

for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, anchor="center", width=120)

tabela.pack(expand=True, fill="both", padx=10, pady=10)

scrollbar = ttk.Scrollbar(aba_historico, orient="vertical", command=tabela.yview)
tabela.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ==============================
# UPDATE UI
# ==============================
def atualizar_log():
    while not log_queue.empty():
        msg = log_queue.get()
        log_box.configure(state="normal")
        log_box.insert("end", msg + "\n")
        log_box.configure(state="disabled")
        log_box.see("end")
    app.after(500, atualizar_log)

def atualizar_ui():
    while not ui_queue.empty():
        tipo, valor = ui_queue.get()

        if tipo == "contador":
            contador_label.configure(text=f"Ocorrências: {valor}")

    app.after(500, atualizar_ui)

def carregar_historico():
    arquivo = "historico_ocorrencias.csv"

    for item in tabela.get_children():
        tabela.delete(item)

    if os.path.isfile(arquivo):
        with open(arquivo, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                tabela.insert("", "end", values=row)

    app.after(5000, carregar_historico)


#=============================
# START
# ==============================
atualizar_log()
atualizar_ui()
carregar_historico()
verificar_inatividade()

app.mainloop()