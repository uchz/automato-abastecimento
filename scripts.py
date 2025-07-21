#SCRIPT PARA ACHAR OS IFRAMES
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
        sidebar = driver.find_element(By.CLASS_NAME, "VCompactBar")
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


from selenium.common.exceptions import NoSuchElementException

driver.switch_to.default_content()
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"Qtd iframes: {len(iframes)}")

for idx, iframe in enumerate(iframes):
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe)
        cells = driver.find_elements(By.CSS_SELECTOR, 'div[col-id="NOMEAREASEP"]')
        print(f"Iframe [{idx}] => Células encontradas: {len(cells)}")
    except Exception as e:
        print(f"Iframe [{idx}] erro: {e}")

driver.switch_to.default_content()