#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# %%

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # REMOVA isso
driver = webdriver.Chrome(options=options)

driver.get('http://sankhya.lleferragens.com.br/mge/')

       

# %%
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
# %%
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

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-input-element"]')))
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys('Etiquetas do volumoso')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys(Keys.ENTER)

#%% #ATUALIZA A PAGINA

driver.refresh()

#%%
#ATUALIZA A PAGINA

# 1) Volta pro contexto raiz
driver.switch_to.default_content()

# 2) Pega o iframe certo
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)


actions = ActionChains(driver)

sidebar = driver.find_element(By.CLASS_NAME, "VCompactBar")
actions = ActionChains(driver)
actions.move_to_element(sidebar).perform()

botao = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-Button")))
botao.click()
sleep(5)
driver.find_element(By.XPATH, '//*[@id="ag-grid#gwt-uid-2"]/sk-application/sk-top-bar/sk-action-button').click()

sleep(2)
actions.send_keys(Keys.DOWN).perform()
sleep(1)
actions.send_keys(Keys.ENTER).perform()
sleep(1)
actions.send_keys(Keys.ESCAPE).perform()


# %% CODIGO ATUALIZADO
driver.switch_to.default_content()

# 2) Pega o iframe certo
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

coluna_cells = driver.find_elements(By.CSS_SELECTOR, 'div[col-id="NOMEAREASEP"]')

coluna_cells[0].click()
sleep(1)
coluna_cells[0].click()

ocs = ['107916']
clicked = 0
for i in ocs:
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    iframe = iframes[6]
    driver.switch_to.frame(iframe)

    sidebar = driver.find_element(By.CLASS_NAME, "VCompactBar")
    actions = ActionChains(driver)
    actions.move_to_element(sidebar).perform()

    wait = WebDriverWait(driver, 240)
    input_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-TextBox")))
    botao = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-Button")))

    input_box.click()
    input_box.send_keys(Keys.BACKSPACE)
    input_box.send_keys(i)

    sleep(2)
    botao.click()
    sleep(10)

    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    iframe = iframes[6]
    driver.switch_to.frame(iframe)

    coluna_cells = driver.find_elements(By.CSS_SELECTOR, 'div[col-id="NOMEAREASEP"]')

    sep_volumoso_cells = [
        cell for cell in coluna_cells if cell.text.strip().startswith("SEP VOLUMOSO")
    ]

    if len(sep_volumoso_cells) >= 2:

        primeiro = sep_volumoso_cells[0]
        ultimo = sep_volumoso_cells[-1]

        actions = ActionChains(driver)

        # Garante que o primeiro está visível
        driver.execute_script("arguments[0].scrollIntoView(true);", primeiro)
        actions.move_to_element(primeiro).click().perform()
        # print(f"✅ Cliquei no primeiro: {primeiro.text.strip()}")
        sleep(2)
        # SHIFT + clique no último
        driver.execute_script("arguments[0].scrollIntoView(true);", ultimo)
        actions.key_down(Keys.SHIFT)
        actions.move_to_element(ultimo).click()
        actions.key_up(Keys.SHIFT)
        actions.perform()
        # print(f"✅ SHIFT + clique no último: {ultimo.text.strip()}")

        sleep(2)
        driver.find_element(By.XPATH, '//*[@id="ag-grid#gwt-uid-2"]/sk-application/sk-top-bar/sk-action-button').click()
        actions.send_keys(Keys.ENTER).perform()
        sleep(3)
        actions.send_keys(Keys.TAB).perform()
        sleep(2)
        actions.send_keys(i).perform()
        sleep(2)
        actions.send_keys(Keys.ENTER).perform()
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div/div/div[3]/div[2]/button')))
        sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[3]/div[2]/button').click()
        sleep(2)
        actions.send_keys(Keys.ESCAPE).perform()
    # Volta pro principal se precisar
    driver.switch_to.default_content()


#%%  SELECIONANDO AS LINHAS DO GRID


#SELECIONANDO AS LINHAS
driver.switch_to.default_content()
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

coluna_cells = driver.find_elements(By.CSS_SELECTOR, 'div[col-id="NOMEAREASEP"]')


print(f"Total de células encontradas: {len(coluna_cells)}")
clicked = 0

# 3) Filtra SEP VOLUMOSO
sep_volumoso_cells = [
    cell for cell in coluna_cells if cell.text.strip().startswith("SEP VOLUMOSO")
]

print(f"➡️ Total SEP VOLUMOSO: {len(sep_volumoso_cells)}")

if len(sep_volumoso_cells) >= 2:

    primeiro = sep_volumoso_cells[0]
    ultimo = sep_volumoso_cells[-1]

    actions = ActionChains(driver)

    # Garante que o primeiro está visível
    driver.execute_script("arguments[0].scrollIntoView(true);", primeiro)
    actions.move_to_element(primeiro).click().perform()
    print(f"✅ Cliquei no primeiro: {primeiro.text.strip()}")

    # SHIFT + clique no último
    driver.execute_script("arguments[0].scrollIntoView(true);", ultimo)
    actions.key_down(Keys.SHIFT)
    actions.move_to_element(ultimo).click()
    actions.key_up(Keys.SHIFT)
    actions.perform()
    print(f"✅ SHIFT + clique no último: {ultimo.text.strip()}")
# Volta pro principal se precisar
    driver.switch_to.default_content()

#    print(j)



#%%
driver.switch_to.default_content()
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)
sleep(2)
driver.find_element(By.XPATH, '//*[@id="ag-grid#gwt-uid-2"]/sk-application/sk-top-bar/sk-action-button').click()
actions.send_keys(Keys.ENTER).perform()
sleep(3)
actions.send_keys(Keys.TAB).perform()
sleep(2)


# sleep(3)
# driver.find_element(By.XPATH, '//*[@id="sk-popover-005"]/div[2]/div/ul/li/div/span').click()


#%%

actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('b').key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
actions.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
sleep(3)
# actions.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

# %%
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
        sidebar = driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[3]/div[2]/button')
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