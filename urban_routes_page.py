import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # --- Selectores principales ---
        self.pickup_input = (By.ID, "from")
        self.destination_input = (By.ID, "to")
        self.initial_request_taxi_button = (By.CSS_SELECTOR, "button.button.round")
        self.comfort_icon = (By.XPATH, "//div[contains(text(),'Comfort')]/parent::div")

        # --- Teléfono ---
        self.phone_input_button = (By.XPATH, "//div[text()='Número de teléfono']")
        self.phone_input_field = (By.NAME, "phone")
        self.phone_submit_button = (By.CSS_SELECTOR, "button.button.full")
        self.code_input_field = (By.ID, "code")
        self.code_submit_button = (By.XPATH, "//button[contains(., 'Confirmar')]")

        # --- Pago ---
        self.payment_modal_button = (
            By.XPATH, "//div[contains(@class,'pp-button') and .//div[text()='Método de pago']]"
        )
        self.payment_method_add_card_button = (
            By.XPATH, "//div[contains(@class,'pp-row') and .//div[text()='Agregar tarjeta']]"
        )
        self.card_number_input = (By.ID, "number")
        # CVV: corregido placeholder de 123
        self.card_cvv_input = (By.XPATH, "//input[@placeholder='123']")
        self.card_link_button = (By.XPATH, "//button[normalize-space()='Agregar']")
        self.payment_modal_container = (By.CSS_SELECTOR, "div.modal.payment-picker")
        self.close_payment_modal_button = (
            By.XPATH, "//div[contains(@class,'payment-picker')]//button[contains(@class,'close-button')]"
        )

        # --- Comentario ---
        self.message_input = (By.NAME, "comment")

        # --- Opciones extra ---
        self.blanket_and_tissues_slider = (
            By.XPATH,
            "//div[./div[@class='r-sw-label' and text()='Manta y pañuelos']]//span[@class='slider round']"
        )
        self.add_ice_cream_button = (
            By.XPATH,
            "//div[./div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-plus']"
        )

        # --- Pedido final ---
        self.final_order_button = (By.XPATH, "//button[contains(., 'Pedir un taxi')]")

    # --- Métodos de flujo ---
    def set_from(self, address):
        field = self.wait.until(EC.element_to_be_clickable(self.pickup_input))
        field.clear()
        field.send_keys(address, Keys.ARROW_DOWN, Keys.ENTER)
        return True

    def set_to(self, address):
        field = self.wait.until(EC.element_to_be_clickable(self.destination_input))
        field.clear()
        field.send_keys(address, Keys.ARROW_DOWN, Keys.ENTER)
        return True

    def click_request_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.initial_request_taxi_button)).click()
        return True

    def select_comfort(self):
        element = self.wait.until(EC.element_to_be_clickable(self.comfort_icon))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.click()
        return True

    def send_phone_number(self, number):
        self.wait.until(EC.element_to_be_clickable(self.phone_input_button)).click()
        phone_field = self.wait.until(EC.presence_of_element_located(self.phone_input_field))
        phone_field.clear()
        phone_field.send_keys(number)
        self.wait.until(EC.element_to_be_clickable(self.phone_submit_button)).click()
        return True

    def confirm_sms_code(self, code):
        try:
            code_field = self.wait.until(EC.presence_of_element_located(self.code_input_field))
            code_field.clear()
            for digit in code:
                code_field.send_keys(digit)
                time.sleep(0.2)  # pausa para disparar validación por dígito

            # Forzar blur/validación
            code_field.send_keys(Keys.TAB)
            time.sleep(1)

            # Intentar clic en Confirmar
            confirm_btn = self.wait.until(EC.presence_of_element_located(self.code_submit_button))
            if confirm_btn.is_enabled():
                confirm_btn.click()
            else:
                # fallback con JS
                self.driver.execute_script("arguments[0].click();", confirm_btn)

            # Esperar a que desaparezca el modal del SMS
            self.wait.until(EC.invisibility_of_element_located(self.code_input_field))
            return True
        except Exception:
            return False

    def add_credit_card(self, number, cvv):
        try:
            # Abrir modal
            self.wait.until(EC.element_to_be_clickable(self.payment_modal_button)).click()
            self.wait.until(EC.element_to_be_clickable(self.payment_method_add_card_button)).click()

            # Ingresar número
            number_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
            number_input.clear()
            for digit in number:
                number_input.send_keys(digit)
                time.sleep(0.05)

            # Buscar campo CVV (soporte a ambos placeholders)
            try:
                cvv_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='123']")))
            except TimeoutException:
                cvv_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='12']")))

            cvv_input.clear()
            for digit in cvv:
                cvv_input.send_keys(digit)
                time.sleep(0.05)
            cvv_input.send_keys(Keys.TAB)
            time.sleep(0.5)

            # Botón Agregar
            add_btn = self.wait.until(EC.presence_of_element_located(self.card_link_button))
            if add_btn.is_enabled():
                add_btn.click()
            else:
                self.driver.execute_script("arguments[0].click();", add_btn)

            # Cerrar modal
            close_btn = self.wait.until(EC.element_to_be_clickable(self.close_payment_modal_button))
            close_btn.click()
            self.wait.until(EC.invisibility_of_element_located(self.payment_modal_container))

            return True
        except Exception:
            return False

    def write_message(self, message):
        self.wait.until(EC.element_to_be_clickable(self.message_input)).send_keys(message)
        return True

    def toggle_blanket_and_tissues(self):
        try:
            slider = self.wait.until(EC.element_to_be_clickable(self.blanket_and_tissues_slider))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", slider)
            slider.click()
            return True
        except Exception:
            try:
                slider = self.wait.until(EC.presence_of_element_located(self.blanket_and_tissues_slider))
                self.driver.execute_script("arguments[0].click();", slider)
                return True
            except Exception:
                return False

    def add_ice_cream(self, quantity=2):
        added = 0
        for _ in range(quantity):
            try:
                btn = self.wait.until(EC.element_to_be_clickable(self.add_ice_cream_button))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                btn.click()
                added += 1
                time.sleep(0.3)
            except Exception:
                try:
                    btn = self.wait.until(EC.presence_of_element_located(self.add_ice_cream_button))
                    self.driver.execute_script("arguments[0].click();", btn)
                    added += 1
                except:
                    break
        return added

    def click_final_order_button(self):
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.final_order_button))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
            button.click()
            return True
        except Exception:
            try:
                button = self.wait.until(EC.presence_of_element_located(self.final_order_button))
                self.driver.execute_script("arguments[0].click();", button)
                return True
            except Exception:
                return False
