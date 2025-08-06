#%% MODULOS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import pandas as pd
# %% TRATAR OS ARQUIVOS
#Procura o arquivo no Desktop
df = pd.read_excel('abastecimento-por-oc.xls', header=2)

#Removendo colunas
df.drop(columns=['TIPOTAREFA', 'DESCDESTINO','DESCORIGEM','CODENDORIGEM','CODENDDESTINO','NUTAREFA', 'DTTAREFA','TIPOTAREFA' ], inplace=True)

df = df[df['PRIORIDADE'] != -999999999]

# Criar uma nova coluna para armazenar os valores atribuídos
df['novo_valor'] = 0

# Inicializar a variável de controle para atribuir valores diferentes
novo_valor = -89

# Criar um dicionário para rastrear o último valor atribuído para cada ordem de carga
ultimo_valor_por_ordem = {}
df.set_index('ORDEMCARGA')

# Iterar sobre as linhas do DataFrame
for index, row in df.iterrows():
    ordem_de_carga = row['ORDEMCARGA']

    # Verificar se a ordem de carga já foi encontrada anteriormente
    if ordem_de_carga not in ultimo_valor_por_ordem:
        # Se não foi encontrada, atribuir um novo valor
        ultimo_valor_por_ordem[ordem_de_carga] = novo_valor
        novo_valor += 1

    # Atribuir o valor à nova coluna
    df.at[index, 'novo_valor'] = ultimo_valor_por_ordem[ordem_de_carga]


# Tirando valores duplicados
df.drop_duplicates(subset=['CODPROD'], inplace=True)



#%%  ABRIR O CHROME
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # REMOVA isso
driver = webdriver.Chrome(options=options)

driver.get('http://sankhya.lleferragens.com.br/mge/')

       

# %% USERNAME
host = driver.find_element(By.CSS_SELECTOR, "sankhya-login")

shadow_root = driver.execute_script('return arguments[0].shadowRoot', host)


container = driver.execute_script(
    'return arguments[0].shadowRoot.querySelector(".account-input-container")',
    host
)

wait = WebDriverWait(container, 10) 
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#user")))
input_element = container.find_element(By.CSS_SELECTOR, "input#user")
input_element.send_keys("luis.henrique")
input_element.send_keys(Keys.ENTER)
# %% PASSWORD
host = driver.find_element(By.CSS_SELECTOR, "sankhya-login")

shadow_root = driver.execute_script('return arguments[0].shadowRoot', host)


container = driver.execute_script(
    'return arguments[0].shadowRoot.querySelector(".account-input-container")',
    host
)

wait = WebDriverWait(container, 10) 
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#password")))
input_element = container.find_element(By.CSS_SELECTOR, "input#password")
input_element.send_keys("22064KIV")
input_element.send_keys(Keys.ENTER)


#%% ENTRANDO NA ABA DA GERENCIA
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-input-element"]')))
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys('Expedição Mercadorias')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys(Keys.ENTER)

#%%# ATUALIZA A PAGINA
sleep(5)
driver.refresh()
# %%

# 1) Volta pro contexto raiz
driver.switch_to.default_content()

# 2) Pega o iframe certo
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

driver.find_element(By.XPATH, '//*[@id="expedicao-mercadoria"]/sk-vbox/sk-hdividedbox/sk-sidenav/div[1]/sk-filter-panel/div/sk-vbox/div[1]/div/sk-personalized-filter/div/div[1]/button').click()


# %%

colunas = ['ORDEMCARGA','DESCRSITUACAO','AreaSeparacao.NOMEAREASEP','AreaConferencia.NOMEAREACONF']

dados_colunas = {}
for col_id in colunas:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", col_id)
    actions.move_to_element(cell).perform()
    elementos = driver.find_elements(By.CSS_SELECTOR, f'div[col-id="{col_id}"]')
    dados_colunas[col_id] = [el.text.strip() for el in elementos]

# Cria o DataFrame
df = pd.DataFrame(dados_colunas)



df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)
# %%
df
# %%
df.to_excel('teste.xlsx')
# %%

col_ids = ['ORDEMCARGA','DESCRSITUACAO','AreaSeparacao.NOMEAREASEP','AreaConferencia.NOMEAREACONF']

linhas_extraidas = []
linhas_hash = set()

# Localiza o container de rolagem do grid (confirme no seu HTML)
grid_container = driver.find_element(By.CSS_SELECTOR, '.ag-body-viewport')

# Número máximo de scrolls seguidos sem novas linhas
max_repeticoes = 10
repeticoes_iguais = 0
ultima_qtd = 0

while True:
    # Aguarda o carregamento dos dados
    sleep(0.3)

    linhas_visiveis = driver.find_elements(By.CSS_SELECTOR, '.ag-row')
    
    for linha in linhas_visiveis:
        dados_linha = {}
        for col_id in col_ids:
            try:
                celula = linha.find_element(By.CSS_SELECTOR, f'div[col-id="{col_id}"]')
                dados_linha[col_id] = celula.text.strip()
            except:
                dados_linha[col_id] = ''

        # Verifica se a linha é válida (completa)
        hash_linha = tuple(dados_linha[col] for col in col_ids)
        if hash_linha not in linhas_hash and any(dados_linha.values()):
            linhas_hash.add(hash_linha)
            linhas_extraidas.append(dados_linha)

    # Verifica se novas linhas foram adicionadas
    qtd_atual = len(linhas_extraidas)
    if qtd_atual == ultima_qtd:
        repeticoes_iguais += 1
        if repeticoes_iguais >= max_repeticoes:
            break
    else:
        repeticoes_iguais = 0
        ultima_qtd = qtd_atual

    # Faz scroll maior (mais agressivo)
    driver.execute_script("arguments[0].scrollTop += 300;", grid_container)

# Cria o DataFrame com todos os dados
df_temp = pd.DataFrame(dados_colunas)

# Usa a primeira linha como cabeçalho, se necessário
df_temp.columns = df_temp.iloc[0]
df = df_temp[1:].reset_index(drop=True)

# Exibe o resultado
print(df)
# %%
df
# %%
