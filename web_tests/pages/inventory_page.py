from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def adicionar_produto_ao_carrinho(self):
        add_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
        self.driver.execute_script("arguments[0].click();", add_btn)

    def ir_para_carrinho(self):
        cart_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", cart_btn)
        self.driver.execute_script("arguments[0].click();", cart_btn)
        self.wait.until(EC.url_contains("cart"))