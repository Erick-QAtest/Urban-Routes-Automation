import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # --- Ruta ---
        self.pickup_input = (By.ID, "from")
        self.destination_input = (By.ID, "to")
        self.initial_request_taxi_button = (By.CSS_SELECTOR, "button.button.round")
        self.comfort_icon = (By.XPATH, "//div[contains(text(),'Comfort')]/parent::div")

        # --- Teléfono ---
        self.phone_input_button = (By.XPATH, "//div[text()='Número de teléfono']")
        self.phone_input_field = (By.NAME, "phone")
        self.phone_submit_button = (By.CSS_SELECTOR, "button.button.full")
        self.code_input_field = (By.ID, "code")  # para SMS
        self.code_submit_button = (By.XPATH, "//button[contains(., 'Confirmar')]")

        # --- Pago / tarjeta ---
        self.payment_modal_button = (
            By.XPATH, "//div[contains(@class, 'pp-button') and .//div[text()='Método de pago']]"
        )
        self.payment_method_add_card_button = (
            By.XPATH, "//div[contains(@class, 'pp-row') and .//div[text()='Agregar tarjeta']]"
        )
        self.card_number_input = (By.ID, "number")
        self.card_cvv_input = (By.XPATH, "//input[@placeholder='12']")  # para tarjeta
        self.card_link_button = (By.XPATH, "//button[contains(text(), 'Agregar')]")
        self.payment_modal_container = (By.CSS_SELECTOR, "div.modal.payment-picker.open")
        self.close_payment_modal_button = (
            By.XPATH,
            "//div[contains(@class, 'payment-picker') and contains(@class, 'open')]//button[contains(@class, 'close-button')]"
        )

        # --- Extras ---
        self.message_input = (By.NAME, "comment")
        self.blanket_and_tissues_slider = (
            By.XPATH,
            "//div[./div[@class='r-sw-label' and text()='Manta y pañuelos']]//span[@class='slider round']"
        )
        self.add_ice_cream_button = (
            By.XPATH,
            "//div[./div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-plus']"
        )

        # --- Confirmación ---
        self.final_order_button = (
            By.XPATH, "//button[@class='smart-button' and .//span[text()='Pedir un taxi']]"
        )
        self.final_modal = (By.XPATH, "//div[contains(@class, 'OrderConfirmationModal')]")

    # --- Helper reutilizable ---
    def safe_click(self, locator):
        """Espera a que desaparezca overlay y hace clic seguro."""
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        except TimeoutException:
            pass

        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    # --- Métodos de flujo ---
    def set_from(self, address):
        input_field = self.wait.until(EC.element_to_be_clickable(self.pickup_input))
        input_field.clear()
        input_field.send_keys(address)
        time.sleep(1)
        input_field.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

    def set_to(self, address):
        input_field = self.wait.until(EC.element_to_be_clickable(self.destination_input))
        input_field.clear()
        input_field.send_keys(address)
        time.sleep(1)
        input_field.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

    def click_request_taxi(self):
        self.safe_click(self.initial_request_taxi_button)

    def select_comfort(self):
        self.safe_click(self.comfort_icon)

    def send_phone_number(self, number):
        self.safe_click(self.phone_input_button)
        phone_field = self.wait.until(EC.presence_of_element_located(self.phone_input_field))
        phone_field.send_keys(number)
        self.safe_click(self.phone_submit_button)

    def confirm_sms_code(self, code):
        code_field = self.wait.until(EC.presence_of_element_located(self.code_input_field))
        code_field.send_keys(code)
        self.safe_click(self.code_submit_button)

    def add_credit_card(self, number, cvv):
        # Abrir modal de pago
        self.safe_click(self.payment_modal_button)

        # Abrir "Agregar tarjeta"
        self.safe_click(self.payment_method_add_card_button)

        # Rellenar número
        number_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        number_input.clear()
        number_input.send_keys(number)

        # Rellenar CVV
        cvv_input = self.wait.until(EC.visibility_of_element_located(self.card_cvv_input))
        cvv_input.clear()
        cvv_input.send_keys(cvv)

        # 🔑 Click fuera de los inputs (formulario) para habilitar el botón
        form_locator = (By.CSS_SELECTOR, "div.section.active.unusual form")
        self.safe_click(form_locator)

        # Confirmar con botón "Agregar"
        self.safe_click(self.card_link_button)

        # Esperar a que se cierre el modal de tarjeta
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.section.active.unusual")))

        # Cerrar modal principal de métodos de pago
        self.safe_click(self.close_payment_modal_button)
        self.wait.until(EC.invisibility_of_element_located(self.payment_modal_container))

    def write_message(self, message):
        self.wait.until(EC.element_to_be_clickable(self.message_input)).send_keys(message)

    def toggle_blanket_and_tissues(self):
        self.safe_click(self.blanket_and_tissues_slider)

    def add_ice_cream(self, quantity=2):
        for _ in range(quantity):
            self.safe_click(self.add_ice_cream_button)
            time.sleep(0.3)

    def click_final_order_button(self):
        self.safe_click(self.final_order_button)

    def wait_for_final_modal(self):
        self.wait.until(EC.visibility_of_element_located(self.final_modal))
