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
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys('Gerencia WMS')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys(Keys.ENTER)

#%%# ATUALIZA A PAGINA
sleep(5)
driver.refresh()

# %% # CÓDIGO ATUALIZADO

# 1) Volta pro contexto raiz
driver.switch_to.default_content()

# 2) Pega o iframe certo
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

prod, prior = ['23861', '608'], ['-88', '-87']

for i, j in zip(df['CODPROD'], df['novo_valor']):
    sleep(3)

    try:
        sidebar = driver.find_elements(By.XPATH, '//*[@id="simple-item-content"]/sk-pesquisa-input/sk-text-input/input')
        sidebar = sidebar[1]
        sidebar.click()
        sleep(2)

        for letra in str(i):
            sidebar.send_keys(letra)
            sleep(0.1)

        sleep(3)

        driver.find_element(By.ID, 'btnAplicar').click()
        sleep(3)

    except (NoSuchElementException, IndexError) as e:
        print(f"⚠️ Erro na pesquisa: {e}")
        continue

    try:
        prioridade = driver.find_elements(By.CSS_SELECTOR, 'div[col-id=PRIORIDADE')
        prioridade = prioridade[1]

        actions = ActionChains(driver)
        actions.double_click(prioridade).perform()
        sleep(2)

        for letra in str(j):
            actions.send_keys(str(letra)).perform()
            sleep(0.1)

        sleep(2)
        actions.send_keys(Keys.F7).perform()
        # actions.send_keys(Keys.ENTER).perform()
        sleep(2)

        for letra in str(j):
            actions.send_keys(str(letra)).perform()
            sleep(0.1)

        sleep(2)
        actions.send_keys(Keys.F7).perform()
        # actions.send_keys(Keys.ENTER).perform()
        sleep(2)

    except (NoSuchElementException, IndexError) as e:
        print(f"⚠️ Erro ao editar prioridade: {e}")
        continue

    try:
        grid_dep = driver.find_elements(By.CSS_SELECTOR, 'div[col-id=POSSUIDEPENDENTE]')
        nao_items = [cell for cell in grid_dep if cell.text.strip() == "Não"]

        if len(nao_items) >= 2:
            primeiro = nao_items[0]
            ultimo = nao_items[-1]

            driver.execute_script("arguments[0].scrollIntoView(true);", primeiro)
            driver.execute_script("arguments[0].scrollIntoView(true);", ultimo)

            actions = ActionChains(driver)
            actions.move_to_element(primeiro).click()
            actions.key_down(Keys.SHIFT)
            actions.move_to_element(ultimo).click()
            actions.key_up(Keys.SHIFT)
            actions.perform()

            print(f"✅ SHIFT + clique de '{primeiro.text.strip()}' até '{ultimo.text.strip()}'")

        elif len(nao_items) == 1:
            unico = nao_items[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", unico)
            actions = ActionChains(driver)
            actions.move_to_element(unico).click().perform()
            print(f"✅ Cliquei no único: '{unico.text.strip()}'")
        else:
            print("🚫 Nenhum 'Não' encontrado.")
            continue

        sleep(5)

        # Tenta botão principal
        button = driver.find_element(By.XPATH, '//*[@id="page"]/sk-application/sk-viewstack/sk-viewstack-content/div/sk-vbox/sk-hbox[3]/sk-hbox[3]/button[1]')
        button.click()

        # Tenta botão de confirmação
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')
        ))
        button1 = driver.find_element(By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')
        button1.click()

        
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')
        ))
        button1 = driver.find_element(By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')
        button1.click()

        


    except(NoSuchElementException, TimeoutException, IndexError) as e:
        print(f"⚠️ Erro na seleção ou confirmação: {e}")
        continue
        
    sleep(3)






# %% TESTE DE IFRAMES
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

driver.switch_to.default_content()

# Conta quantos iframes tem na HORA de executar cada iteração:
total_iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"Total iframes: {len(total_iframes)}")

found = False

for idx in range(len(total_iframes)):
    
    driver.switch_to.default_content()

    # 🔑 Rebusca os iframes atualizados
    try:
        iframes_now = driver.find_elements(By.TAG_NAME, "iframe")
        iframe = iframes_now[idx]
    except IndexError:
        print(f"Iframe {idx} não existe mais.")
        continue

    # Tenta pegar id
    try:
        iframe_id = iframe.get_attribute('id')
    except StaleElementReferenceException:
        print(f"Iframe {idx} está stale.")
        continue

    print(f"\nTestando iframe [{idx}] ID: {iframe_id}")

    try:
        driver.switch_to.frame(iframe)
    except Exception as e:
        print(f"Erro ao entrar no iframe [{idx}]: {e}")
        continue

    # Tenta achar o elemento dentro do iframe
    try:
        sidebar = driver.find_element(By.XPATH, '//*[@id="simple-item-content"]/sk-pesquisa-input/sk-text-input/input')
        print(f"✅ Sidebar encontrada no iframe [{idx}]")
        found = True
        break
    except NoSuchElementException:
        print(f"❌ Sidebar NÃO encontrada no iframe [{idx}]")
    except Exception as e:
        print(f"⚠️ Erro inesperado dentro do iframe [{idx}]: {e}")

driver.switch_to.default_content()

if not found:
    print("🚫 Sidebar não encontrada em nenhum iframe.")
# %%



# 1) Volta pro contexto raiz
driver.switch_to.default_content()

# 2) Pega o iframe certo
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

prod, prior = [13159, 85580], ['-88', '-87']

for i,j in zip(prod,prior ):

    sleep(4)

    sidebar = driver.find_elements(By.XPATH, '//*[@id="simple-item-content"]/sk-pesquisa-input/sk-text-input/input')
    actions = ActionChains(driver)

    sidebar = sidebar[1]

    sidebar.click()
    sleep(1)
    sidebar.send_keys(i)
    sleep(1)
    driver.find_element(By.ID, 'btnAplicar').click()
    sleep(5)

    prioridade = driver.find_elements(By.CSS_SELECTOR, 'div[col-id=PRIORIDADE')
    prioridade = prioridade[1]

    actions.double_click(prioridade).perform()
    sleep(2)
    for letra in j:
        actions.send_keys(str(letra)).perform()
        sleep(0.1)
        
    sleep(2)
    actions.send_keys(Keys.F7).perform()
    sleep(5)

    grid_dep = driver.find_elements(By.CSS_SELECTOR, 'div[col-id=POSSUIDEPENDENTE]')

    nao_items = [cell for cell in grid_dep if cell.text.strip() == "Não"]

    if len(nao_items) >= 2:

        primeiro = nao_items[0]
        ultimo = nao_items[-1]

        driver.execute_script("arguments[0].scrollIntoView(true);", primeiro)
        driver.execute_script("arguments[0].scrollIntoView(true);", ultimo)

        actions = ActionChains(driver)
        actions.move_to_element(primeiro).click()
        actions.key_down(Keys.SHIFT)
        actions.move_to_element(ultimo).click()
        actions.key_up(Keys.SHIFT)
        actions.perform()

        sleep(10)
        button = driver.find_element(By.XPATH, '//*[@id="page"]/sk-application/sk-viewstack/sk-viewstack-content/div/sk-vbox/sk-hbox[3]/sk-hbox[3]/button[1]')

        button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')))

        button1 = driver.find_element(By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')

        button1.click()

        print(f"✅ SHIFT + clique de '{primeiro.text.strip()}' até '{ultimo.text.strip()}'")

    elif len(nao_items) == 1:
        unico = nao_items[0]
        driver.execute_script("arguments[0].scrollIntoView(true);", unico)

        actions = ActionChains(driver)
        actions.move_to_element(unico).click().perform()

        print(f"✅ Cliquei no único: '{unico.text.strip()}'")

        sleep(10)

        button = driver.find_element(By.XPATH, '//*[@id="page"]/sk-application/sk-viewstack/sk-viewstack-content/div/sk-vbox/sk-hbox[3]/sk-hbox[3]/button[1]')

        button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')))

        button1 = driver.find_element(By.XPATH, '//*[@id="GerenciaDoWMSApp"]/body/div[5]/div/div/div[3]/div[2]/button[2]')

        button1.click()


    else:
        print("🚫 Nenhum 'Não' encontrado.")