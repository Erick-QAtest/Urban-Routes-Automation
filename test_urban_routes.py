import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urban_routes_page import UrbanRoutesPage
from utils import retrieve_phone_code
import data


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        """Configura el driver y la clase de página una sola vez antes de todas las pruebas."""
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        """Cierra el driver una sola vez al final de todas las pruebas."""
        cls.driver.quit()

    def test_set_route(self):
        """Prueba 1: Confirma el establecimiento de la ruta."""
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        # Assert que el botón de petición inicial se vuelve visible
        self.routes_page.wait.until(
            EC.visibility_of_element_located(self.routes_page.initial_request_taxi_button)
        )
        assert self.driver.find_element(*self.routes_page.initial_request_taxi_button).is_displayed()

    def test_set_comfort(self):
        """Prueba 2: Verifica que se selecciona la tarifa Comfort."""
        self.routes_page.click_request_taxi()
        self.routes_page.select_comfort()
        # Assert que el icono de Comfort está activo
        comfort_class = self.routes_page.wait.until(
            EC.presence_of_element_located(self.routes_page.comfort_icon)
        )
        assert "active" in comfort_class.get_attribute("class")

    def test_set_phone_number(self):
        """Prueba 3: Prueba para agregar número de teléfono."""
        self.routes_page.send_phone_number(data.phone_number)
        # Assert que el campo de código SMS aparece
        self.routes_page.wait.until(EC.visibility_of_element_located(self.routes_page.code_input_field))
        assert self.driver.find_element(*self.routes_page.code_input_field).is_displayed()

    def test_confirm_sms_code(self):
        """Prueba 4: Prueba para confirmar el código SMS."""
        time.sleep(2)  # espera a que el backend devuelva el SMS
        code = retrieve_phone_code(self.driver)
        self.routes_page.confirm_sms_code(code)
        # Assert que el modal de código se cierra y aparece botón de pago
        self.routes_page.wait.until(EC.element_to_be_clickable(self.routes_page.payment_modal_button))
        assert self.driver.find_element(*self.routes_page.payment_modal_button).is_displayed()

    def test_add_card(self):
        """Prueba 5: Prueba que agrega tarjeta de crédito."""
        self.routes_page.add_credit_card(data.card_number, data.card_cvv)
        # Assert: el modal se cierra y la tarjeta queda seleccionada
        self.routes_page.wait.until(EC.invisibility_of_element_located(self.routes_page.payment_modal_container))
        selected_card = self.driver.find_element(By.ID, "card-1")
        assert selected_card.is_selected()

    def test_write_message(self):
        """Prueba 6: Verifica que se puede enviar un mensaje para el conductor."""
        msg = "Gracias por pasar por mí"
        self.routes_page.write_message(msg)
        message_field = self.routes_page.wait.until(
            EC.presence_of_element_located(self.routes_page.message_input)
        )
        assert message_field.get_attribute("value") == msg

    def test_toggle_blanket(self):
        """Prueba 7: Verifica que se pueda solicitar una frazada."""
        self.routes_page.toggle_blanket_and_tissues()
        # Assert: el slider cambia de estado (ej. checked en input asociado)
        slider = self.routes_page.wait.until(
            EC.presence_of_element_located(self.routes_page.blanket_and_tissues_slider)
        )
        assert "active" in slider.get_attribute("class") or "checked" in self.driver.page_source

    def test_add_icecream(self):
        """Prueba 8: Verifica que se añadieron helados."""
        self.routes_page.add_ice_cream(quantity=2)
        counter_label = self.routes_page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[./div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-value']")
            )
        )
        assert counter_label.text.strip() == "2"
