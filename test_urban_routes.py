import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from data import url, pickup_address, destination_address, phone_number, card_code, message_for_driver
from utils import retrieve_phone_code
from urban_routes_page import UrbanRoutesPage

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        options.add_argument('--disable-logging')  # Opcional: oculta logs de consola
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.driver.get(url)
        cls.page = UrbanRoutesPage(cls.driver)

    def test_full_order(self):
        # Paso 1: Direcciones
        self.page.set_address(pickup_address, destination_address)

        # Paso 2: Tarifa Comfort
        self.page.select_comfort_tariff()

        # Paso 3: Número de teléfono
        self.page.enter_phone_number(phone_number)

        # Paso 4: Tarjeta
        number, cvv = card_code
        self.page.add_credit_card(number, cvv)

        # Espera el código automático
        retrieve_phone_code(self.driver)

        # Paso 5: Mensaje al conductor
        self.page.write_message(message_for_driver)

        # Paso 6: Manta y pañuelos
        self.page.select_blanket_and_tissues()

        # Paso 7: Dos helados
        self.page.add_ice_creams(2)

        # Paso 8: Pedir taxi
        self.page.order_taxi()

        # Paso 9: Verifica que se muestre la info del conductor
        self.page.wait_for_driver_modal()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
