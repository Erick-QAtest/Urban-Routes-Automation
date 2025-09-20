import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import data
from urban_routes_page import UrbanRoutesPage
from utils import retrieve_phone_code


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)
        cls.page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        assert self.page.set_from(data.address_from)
        assert self.page.set_to(data.address_to)
        assert self.page.click_request_taxi()

    def test_set_comfort(self):
        assert self.page.select_comfort()

    def test_set_phone_number(self):
        assert self.page.send_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)  # fallback = "0000" si no encuentra
        assert self.page.confirm_sms_code(code)

    def test_add_card(self):
        assert self.page.add_credit_card(data.card_number, data.card_cvv)

    def test_write_message(self):
        assert self.page.write_message("Gracias por pasar por mí")

    def test_blanket(self):
        assert self.page.toggle_blanket_and_tissues()

    def test_add_ice_cream(self):
        assert self.page.add_ice_cream(2) == 2

    def test_find_driver(self):
        assert self.page.click_final_order_button()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
