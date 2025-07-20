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

driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys('Etiquetas do volumoso')
sleep(2)
driver.find_element(By.XPATH, '//*[@id="search-input-element"]').send_keys(Keys.ENTER)


# %%

# 1) Volta pro contexto raiz
driver.switch_to.default_content()

# 2) Pega o iframe certo
iframes = driver.find_elements(By.TAG_NAME, "iframe")
iframe = iframes[6]
driver.switch_to.frame(iframe)

# %%
ocs = ['107819', '107820', '107821', '107822']

for i in ocs:
    # 3) Localiza a barra flutuante
    sidebar = driver.find_element(By.CLASS_NAME, "VCompactBar")

    # 4) Faz hover na barra
    actions = ActionChains(driver)
    actions.move_to_element(sidebar).perform()
    print("✅ Mouse passado sobre a barra flutuante")

    # 5) Aguarda o input aparecer (ajuste o seletor se precisar!)
    wait = WebDriverWait(driver, 10)
    input_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-TextBox")))

    # 6) Digita
    input_box.click()
    # input_box.click()
    input_box.send_keys(Keys.BACKSPACE)
    input_box.send_keys(i)
    sleep(3)
    input_box.send_keys(Keys.ENTER)
# %%

container = driver.find_element(By.CLASS_NAME, 'ag-center-cols-container')

span = container.find_elements(By.TAG_NAME, 'span')
for j in span:
   
   j = j.text
   
   print(j)
# %%



# %%
# 3) Localiza a barra flutuante
sidebar = driver.find_element(By.CLASS_NAME, "VCompactBar")

# 4) Faz hover na barra
actions = ActionChains(driver)
actions.move_to_element(sidebar).perform()
print("✅ Mouse passado sobre a barra flutuante")



# 5) Aguarda o input aparecer (ajuste o seletor se precisar!)
wait = WebDriverWait(driver, 10)
input_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-TextBox")))

# 6) Digita
input_box.send_keys("107819")
input_box.send_keys(Keys.ENTER)


# 7) Volta pro contexto raiz se quiser continuar fora do iframe
driver.switch_to.default_content()

# %%
