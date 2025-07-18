#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
# %%

driver = webdriver.Chrome()

driver.get('http://sankhya.lleferragens.com.br/mge/')
# %%
host = driver.find_element(By.CSS_SELECTOR, "sankhya-login")

shadow_root = driver.execute_script('return arguments[0].shadowRoot', host)


container = driver.execute_script(
    'return arguments[0].shadowRoot.querySelector(".account-input-container")',
    host
)
# %%
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
input_element = container.find_element(By.CSS_SELECTOR, "input#password")
input_element.send_keys("22064KIV")
input_element.send_keys(Keys.ENTER)
# %%

driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys('Gerencia do WMS')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys(Keys.ENTER)

# %%

input_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//input[contains(@class, 'form-control') and @type='text']"
    ))
)

input_element.send_keys('TESTE')
# %%
# Clique em algo para abrir o formulário
abrir = driver.find_element(By.XPATH, "//sk-icon[@icon='search']")
abrir.click()

# Agora espere o input
input_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//input[contains(@class, 'form-control') and @type='text']"
    ))
)

input_element.send_keys("SEU TEXTO AQUI")
# %%
driver.find_element(By.XPATH, '//*[@id="simple-item-content"]/sk-pesquisa-input/sk-icon')
# %%
