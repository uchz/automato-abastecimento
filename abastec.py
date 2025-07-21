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
# %%

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
# %%

wait = WebDriverWait(container, 10) 
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#password")))
input_element = container.find_element(By.CSS_SELECTOR, "input#password")
input_element.send_keys("22064KIV")
input_element.send_keys(Keys.ENTER)
# %%
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-input-element"]')))
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys('Gerencia WMS')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys(Keys.ENTER)

#%%

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

sidebar = driver.find_elements(By.XPATH, '//*[@id="simple-item-content"]/sk-pesquisa-input/sk-text-input/input')
actions = ActionChains(driver)

sidebar = sidebar[1]

sidebar.click()
sleep(1)
sidebar.send_keys('20917')

driver.find_element(By.ID, 'btnAplicar').click()
sleep(5)
#%%

prioridade = driver.find_elements(By.CSS_SELECTOR, 'div[col-id=PRIORIDADE')

prioridade[1].click()
actions.send_keys(Keys.ENTER).perform()
prioridade[1].click()




# grid.send_keys()

# %%
driver.switch_to.default_content()
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

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
# %%




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
        sidebar = driver.find_element(By.CSS_SELECTOR, 'div[col-id="POSSUIDEPENDENTE"]')
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
