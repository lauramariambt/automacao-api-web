from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def ir_para_checkout(self):
        checkout_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkout_btn)
        self.driver.execute_script("arguments[0].click();", checkout_btn)
        self.wait.until(EC.url_contains("checkout-step-one"))

    def preencher_dados(self, primeiro_nome, ultimo_nome, cep):
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        for field_id, value in [("first-name", primeiro_nome), ("last-name", ultimo_nome), ("postal-code", cep)]:
            self.driver.execute_script("""
                var field = document.getElementById(arguments[0]);
                var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(field, arguments[1]);
                field.dispatchEvent(new Event('input', { bubbles: true }));
                field.dispatchEvent(new Event('change', { bubbles: true }));
            """, field_id, value)

    def continuar(self):
        continue_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        self.driver.execute_script("arguments[0].click();", continue_btn)
        self.wait.until(EC.url_contains("checkout-step-two"))

    def finalizar(self):
        finish_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "finish")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", finish_btn)
        self.driver.execute_script("arguments[0].click();", finish_btn)
        self.wait.until(EC.url_contains("checkout-complete"))