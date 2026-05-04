from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from web_tests.config import BASE_URL


def test_fluxo_compra():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(BASE_URL)

        # login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        wait.until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url

        # adiciona produto ao carrinho
        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
        driver.execute_script("arguments[0].click();", add_btn)

        # acessa carrinho
        cart_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
        driver.execute_script("arguments[0].scrollIntoView(true);", cart_btn)
        driver.execute_script("arguments[0].click();", cart_btn)

        wait.until(EC.url_contains("cart"))
        item = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
        assert item is not None

        # checkout
        checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_btn)
        driver.execute_script("arguments[0].click();", checkout_btn)

        wait.until(EC.url_contains("checkout-step-one"))

        # preenche dados via JavaScript
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        driver.execute_script("document.getElementById('first-name').value = 'Laura'")
        driver.execute_script("document.getElementById('last-name').value = 'Teste'")
        driver.execute_script("document.getElementById('postal-code').value = '12345'")

        # continua fluxo
        continue_btn = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        driver.execute_script("arguments[0].click();", continue_btn)

        import time
        time.sleep(3)
        print("URL após continue:", driver.current_url)
        print("Título da página:", driver.title)

        wait.until(EC.url_contains("checkout-step-two"))

        # finaliza compra
        finish_btn = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
        driver.execute_script("arguments[0].scrollIntoView(true);", finish_btn)
        driver.execute_script("arguments[0].click();", finish_btn)

        wait.until(EC.url_contains("checkout-complete"))
        assert "checkout-complete" in driver.current_url

    finally:
        driver.quit()