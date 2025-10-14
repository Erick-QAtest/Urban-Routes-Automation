import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urban_routes_page import UrbanRoutesPage
from utils import retrieve_phone_code
import data

# Configuración del logger para salida legible en consola
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@pytest.mark.usefixtures()
class TestUrbanRoutes:
    """End-to-End UI Test Suite for Urban Routes | Selenium + Pytest"""

    @classmethod
    def setup_class(cls):
        """Setup: Initialize Chrome driver and open Urban Routes app."""
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)
        logging.info("✅ Browser launched and Urban Routes loaded successfully.")

    @classmethod
    def teardown_class(cls):
        """Teardown: Close browser session after tests."""
        cls.driver.quit()
        logging.info("🧹 Browser closed. Test session completed.")

    @pytest.mark.smoke
    def test_set_route(self):
        """[Smoke] GIVEN valid addresses WHEN user sets origin and destination THEN route should be visible."""
        logging.info("Setting route from '%s' to '%s'", data.address_from, data.address_to)
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.wait.until(
            EC.visibility_of_element_located(self.routes_page.initial_request_taxi_button)
        )
        assert self.driver.find_element(*self.routes_page.initial_request_taxi_button).is_displayed()
        logging.info("✅ Route successfully set.")

    @pytest.mark.regression
    def test_set_comfort(self):
        """[Regression] WHEN Comfort tariff is selected THEN Comfort icon should be active."""
        logging.info("Selecting Comfort tariff.")
        self.routes_page.click_request_taxi()
        self.routes_page.select_comfort()
        comfort_class = self.routes_page.wait.until(
            EC.presence_of_element_located(self.routes_page.comfort_icon)
        )
        assert "active" in comfort_class.get_attribute("class")
        logging.info("✅ Comfort tariff successfully selected.")

    @pytest.mark.regression
    def test_set_phone_number(self):
        """[Regression] WHEN phone number is entered THEN SMS code input should appear."""
        logging.info("Entering phone number: %s", data.phone_number)
        self.routes_page.send_phone_number(data.phone_number)
        self.routes_page.wait.until(EC.visibility_of_element_located(self.routes_page.code_input_field))
        assert self.driver.find_element(*self.routes_page.code_input_field).is_displayed()
        logging.info("✅ Phone number accepted. SMS code input displayed.")

    @pytest.mark.regression
    def test_confirm_sms_code(self):
        """[Regression] GIVEN a valid SMS code WHEN confirmed THEN payment modal button should appear."""
        logging.info("Retrieving SMS code from network logs.")
        time.sleep(2)
        code = retrieve_phone_code(self.driver)
        self.routes_page.confirm_sms_code(code)
        self.routes_page.wait.until(EC.element_to_be_clickable(self.routes_page.payment_modal_button))
        assert self.driver.find_element(*self.routes_page.payment_modal_button).is_displayed()
        logging.info("✅ SMS code confirmed successfully.")

    @pytest.mark.regression
    def test_add_card(self):
        """[Regression] WHEN user adds a credit card THEN card should be stored and visible."""
        logging.info("Adding test card ending in 4242.")
        self.routes_page.add_credit_card(data.card_number, data.card_cvv)
        self.routes_page.wait.until(EC.invisibility_of_element_located(self.routes_page.payment_modal_container))
        selected_card = self.driver.find_element(By.ID, "card-1")
        assert selected_card.is_selected()
        logging.info("✅ Card added and selected successfully.")

    @pytest.mark.regression
    def test_write_message(self):
        """[Regression] WHEN message is written THEN input should contain the same text."""
        msg = "Gracias por pasar por mí"
        logging.info("Writing message to driver: '%s'", msg)
        self.routes_page.write_message(msg)
        message_field = self.routes_page.wait.until(
            EC.presence_of_element_located(self.routes_page.message_input)
        )
        assert message_field.get_attribute("value") == msg
        logging.info("✅ Message field correctly filled.")

    @pytest.mark.regression
    def test_toggle_blanket(self):
        """[Regression] WHEN blanket and tissues are toggled THEN slider should become active."""
        logging.info("Toggling blanket & tissues option.")
        self.routes_page.toggle_blanket_and_tissues()
        slider = self.routes_page.wait.until(
            EC.presence_of_element_located(self.routes_page.blanket_and_tissues_slider)
        )
        assert "active" in slider.get_attribute("class") or "checked" in self.driver.page_source
        logging.info("✅ Blanket & tissues option activated.")

    @pytest.mark.regression
    def test_add_icecream(self):
        """[Regression] WHEN adding ice creams THEN counter should display correct quantity."""
        logging.info("Adding 2 ice creams to the order.")
        self.routes_page.add_ice_cream(quantity=2)
        counter_label = self.routes_page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[./div[@class='r-counter-label' and text()='Helado']]//div[@class='counter-value']")
            )
        )
        assert counter_label.text.strip() == "2"
        logging.info("✅ Ice cream quantity successfully updated.")

