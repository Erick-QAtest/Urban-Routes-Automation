import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20) # Keep at 20 seconds for robustness

        self.pickup_input = (By.ID, "from")
        self.destination_input = (By.ID, "to")
        self.initial_request_taxi_button = (By.CSS_SELECTOR, "button.button.round")

        self.comfort_icon = (By.XPATH, "//div[contains(text(),'Comfort')]/parent::div")

        self.phone_input_button = (By.XPATH, "//div[text()='Número de teléfono']")
        self.phone_input_field = (By.NAME, "phone")
        self.phone_submit_button = (By.CSS_SELECTOR, "button.button.full")

        self.code_input_field = (By.ID, "code")
        self.code_submit_button = (By.XPATH, "//button[contains(., 'Confirmar')]")

        self.payment_modal_button = (By.XPATH, "//div[contains(@class, 'pp-button') and .//div[text()='Método de pago']]")
        self.payment_method_add_card_button = (By.XPATH, "//div[contains(@class, 'pp-row') and .//div[text()='Agregar tarjeta']]")

        self.card_number_input = (By.ID, "number")
        self.card_cvv_input = (By.XPATH, "//input[@placeholder='12']")
        self.card_link_button = (By.XPATH, "//button[contains(text(), 'Agregar')]")

        self.payment_modal_container = (By.CSS_SELECTOR, "div.modal.payment-picker.open")
        self.close_payment_modal_button = (By.XPATH, "//div[contains(@class, 'payment-picker') and contains(@class, 'open')]//button[contains(@class, 'close-button')]")

        self.message_input = (By.NAME, "comment")

        self.blanket_and_tissues_slider = (
            By.XPATH,
            "//div[./div[@class='r-sw-label' and text()='Manta y pañuelos']]//span[@class='slider round']"
        )

        self.add_ice_cream_button = (
            By.XPATH,
            "//div[./div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-plus']"
        )

        self.final_order_button = (By.XPATH, "//button[@class='smart-button' and .//span[text()='Pedir un taxi']]")

        # Keeping this for now, but be prepared to adjust if it's not a modal or locator changes.
        self.final_modal = (By.XPATH, "//div[contains(@class, 'OrderConfirmationModal')]")

    def set_from(self, address):
        input_field = self.wait.until(EC.element_to_be_clickable(self.pickup_input))
        input_field.clear()
        input_field.send_keys(address)
        time.sleep(1)
        input_field.send_keys(Keys.ARROW_DOWN)
        input_field.send_keys(Keys.ENTER)
        print(f"✅ Origen '{address}' establecido.")

    def set_to(self, address):
        input_field = self.wait.until(EC.element_to_be_clickable(self.destination_input))
        input_field.clear()
        input_field.send_keys(address)
        time.sleep(1)
        input_field.send_keys(Keys.ARROW_DOWN)
        input_field.send_keys(Keys.ENTER)
        print(f"✅ Destino '{address}' establecido.")

    def click_request_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.initial_request_taxi_button)).click()
        print("✅ Botón 'Pedir un taxi' (inicial) clicado.")

    def select_comfort(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.comfort_icon))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            print("✅ Comfort seleccionado.")
        except Exception as e:
            print(f"⚠️ No se pudo seleccionar Comfort: {e}. Asegúrate de que el elemento esté visible y clicable.")

    def send_phone_number(self, number):
        self.wait.until(EC.element_to_be_clickable(self.phone_input_button)).click()
        phone_field = self.wait.until(EC.presence_of_element_located(self.phone_input_field))
        phone_field.send_keys(number)
        self.wait.until(EC.element_to_be_clickable(self.phone_submit_button)).click()
        print(f"✅ Número de teléfono '{number}' enviado.")

    def confirm_sms_code(self, code):
        code_field = self.wait.until(EC.presence_of_element_located(self.code_input_field))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", code_field)
        code_field.send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.code_submit_button)).click()
        print(f"✅ Código SMS '{code}' confirmado.")

    def add_credit_card(self, number, cvv):
        print("💳 Intentando añadir tarjeta de crédito...")
        self.wait.until(EC.element_to_be_clickable(self.payment_modal_button)).click()
        print("✅ Botón 'Método de pago' clicado.")

        try:
            add_card_button = self.wait.until(EC.visibility_of_element_located(self.payment_method_add_card_button))
            add_card_button.click()
            print("✅ Botón 'Agregar tarjeta' clicado.")
        except TimeoutException:
            print(f"❌ ERROR: El botón 'Agregar tarjeta' no apareció o no fue clicable dentro del tiempo. Revisa el estado del modal de pago.")
            self.driver.save_screenshot("add_card_button_timeout.png")
            raise

        number_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", number_input)
        number_input.clear()
        for char in number:
            number_input.send_keys(char)
            time.sleep(0.05)
        print("✅ Número de tarjeta ingresado.")

        try:
            cvv_input = self.wait.until(EC.presence_of_element_located(self.card_cvv_input))
            cvv_input.clear()
            for char in cvv:
                cvv_input.send_keys(char)
                time.sleep(0.05)
            self.driver.execute_script("arguments[0].blur();", cvv_input)
            time.sleep(0.5)
            print("✅ CVV ingresado correctamente.")
        except Exception as e:
            print(f"⚠️ Error al ingresar CVV o CVV no visible/requerido: {e}")

        try:
            print("🧲 Haciendo clic en botón 'Agregar' para vincular la tarjeta...")
            self.wait.until(EC.element_to_be_clickable(self.card_link_button)).click()
            print("✅ Tarjeta agregada.")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ No se pudo hacer clic en 'Agregar' para vincular la tarjeta: {e}")

        try:
            print("🔐 Intentando cerrar el modal de método de pago...")
            close_button = self.wait.until(EC.element_to_be_clickable(self.close_payment_modal_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
            close_button.click()
            print("✅ Botón de cerrar modal clicado.")
            self.wait.until(EC.invisibility_of_element_located(self.payment_modal_container))
            print("✅ Modal de método de pago cerrado exitosamente.")
        except Exception as e:
            print(f"❌ ERROR: No se pudo cerrar el modal de método de pago: {e}. La prueba podría fallar más adelante.")

    def write_message(self, message):
        self.wait.until(EC.element_to_be_clickable(self.message_input)).send_keys(message)
        print(f"✅ Mensaje '{message}' ingresado.")

    def toggle_blanket_and_tissues(self):
        print("🧣 Intentando activar manta y pañuelos...")
        try:
            self.driver.execute_script("window.scrollBy(0, 500);")
            slider_element = self.wait.until(EC.element_to_be_clickable(self.blanket_and_tissues_slider))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider_element)
            slider_element.click()
            print("✅ Manta y pañuelos activados.")
        except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            print(f"⚠️ No se pudo activar la manta y pañuelos: {e}. Reintentando con JS click...")
            try:
                slider_element = self.wait.until(EC.presence_of_element_located(self.blanket_and_tissues_slider))
                self.driver.execute_script("arguments[0].click();", slider_element)
                print("✅ Manta y pañuelos activados (vía JS click).")
            except Exception as js_e:
                print(f"❌ Falló el intento de activar manta y pañuelos (JS click): {js_e}. Revisa el locator o la visibilidad.")
                raise

    def add_ice_cream(self, quantity=2):
        print(f"🍦 Agregando {quantity} helados...")
        for i in range(quantity):
            try:
                self.driver.execute_script("window.scrollBy(0, 300);")
                ice_cream_button = self.wait.until(EC.element_to_be_clickable(self.add_ice_cream_button))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ice_cream_button)
                ice_cream_button.click()
                print(f"✅ Helado {i+1} agregado.")
                time.sleep(0.3)
            except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
                print(f"⚠️ No se pudo agregar helado #{i+1}: {e}. Reintentando con JS click...")
                try:
                    ice_cream_button = self.wait.until(EC.presence_of_element_located(self.add_ice_cream_button))
                    self.driver.execute_script("arguments[0].click();", ice_cream_button)
                    print(f"✅ Helado {i+1} agregado (vía JS click).")
                    time.sleep(0.3)
                except Exception as js_e:
                    print(f"❌ Falló el intento de agregar helado #{i+1} (JS click): {js_e}. Revisa el locator o la visibilidad.")
                break

    # Method to click the final "Pedir un taxi" button
    def click_final_order_button(self):
        print("🚕 Intentando clic en el botón FINAL 'Pedir un taxi' para confirmar el pedido...")
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.final_order_button))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            button.click()
            print("✅ Botón FINAL 'Pedir un taxi' clicado exitosamente.")
        except (TimeoutException, ElementClickInterceptedException) as e:
            print(f"❌ ERROR: No se pudo hacer clic en el botón FINAL 'Pedir un taxi': {e}.")
            self.driver.save_screenshot("final_order_button_error.png")
            raise

    def wait_for_final_modal(self):
        print("📦 Esperando confirmación final del pedido...")
        # Adding a small explicit sleep here. This is often necessary after a final action
        # that triggers server processing or a heavy UI transition before the final element appears.
        time.sleep(3) # Give it 3 seconds just in case, this is often the magic number for final modals.
        try:
            self.wait.until(EC.visibility_of_element_located(self.final_modal))
            print("🎉 ¡Modal de confirmación de pedido visible! Pedido completado con éxito.")
        except Exception as e:
            print(f"❌ ERROR: El modal de confirmación final no apareció dentro del tiempo esperado: {e}. El pedido podría no haberse completado.")
            self.driver.save_screenshot("final_modal_error.png") # Screenshot on failure is key
            raise