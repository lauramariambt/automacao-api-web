from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from web_tests.config import BASE_URL
from web_tests.pages.login_page import LoginPage
from web_tests.pages.inventory_page import InventoryPage
from web_tests.pages.checkout_page import CheckoutPage


def test_fluxo_compra():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(BASE_URL)

        LoginPage(driver).login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver)
        inventory.adicionar_produto_ao_carrinho()
        inventory.ir_para_carrinho()

        wait = WebDriverWait(driver, 20)
        item = wait.until(EC.presence_of_element_located(("class name", "inventory_item_name")))
        assert item is not None

        checkout = CheckoutPage(driver)
        checkout.ir_para_checkout()
        checkout.preencher_dados("Laura", "Teste", "12345")
        checkout.continuar()
        checkout.finalizar()

        assert "checkout-complete" in driver.current_url

    finally:
        driver.quit()