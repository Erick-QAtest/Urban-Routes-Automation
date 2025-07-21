import pytest
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

from webdriver_manager.chrome import ChromeDriverManager
from urban_routes_page import UrbanRoutesPage
import data # Assuming data.py exists and contains urban_routes_url, address_from, etc.


def retrieve_phone_code(driver):
    code = None
    for _ in range(10): # Try up to 10 times to get the code
        try:
            logs = driver.get_log("performance")
            for log_entry in reversed(logs):
                # Ensure the message key exists before trying to parse
                if "message" in log_entry:
                    message = json.loads(log_entry["message"])["message"]
                    url = message.get("params", {}).get("request", {}).get("url", "")
                    if "api/v1/number?number" in url:
                        request_id = message["params"]["requestId"]
                        body = driver.execute_cdp_cmd(
                            "Network.getResponseBody", {"requestId": request_id}
                        )
                        # Ensure 'body' exists and is a string before iterating
                        if body and 'body' in body and isinstance(body['body'], str):
                            code = ''.join([x for x in body['body'] if x.isdigit()])
                            if code:
                                return code
        except WebDriverException:
            time.sleep(1) # Wait a bit if there's a WebDriver issue with logs
        except json.JSONDecodeError:
            # Handle cases where log_entry["message"] is not valid JSON
            continue
    raise Exception("❌ No se encontró el código de confirmación del teléfono.")


class TestUrbanRoutes:
    def setup_method(self):
        options = Options()
        # Enable performance logging to capture network requests for phone code
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        # Automatically download and manage chromedriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window() # Maximize window for better element visibility

    def teardown_method(self):
        self.driver.quit() # Close the browser after each test

    def test_full_order(self):
        self.driver.get(data.urban_routes_url) # Navigate to the application URL
        page = UrbanRoutesPage(self.driver) # Initialize the Page Object

        # 1. Set 'from' and 'to' addresses
        page.set_from(data.address_from)
        page.set_to(data.address_to)

        # 2. Click the initial "Pedir un taxi" button
        page.click_request_taxi() # This now calls the method using initial_request_taxi_button

        # 3. Select Comfort class
        page.select_comfort()

        # 4. Send phone number and confirm SMS code
        page.send_phone_number(data.phone_number)
        print("⌛ Esperando código desde logs...")
        time.sleep(2) # Give some time for the network log to appear
        code = retrieve_phone_code(self.driver)
        page.confirm_sms_code(code)

        # 5. Add credit card details
        page.add_credit_card(data.card_number, data.card_cvv)

        # 6. Write message for the driver
        page.write_message("Gracias por pasar por mí")

        # 7. Toggle blanket and tissues option
        page.toggle_blanket_and_tissues()

        # 8. Add ice cream
        page.add_ice_cream(quantity=2)

        # 9. Click the FINAL "Pedir un taxi" button to confirm the order
        # THIS IS THE CRUCIAL NEW STEP
        page.click_final_order_button()


        print("✅ Flujo de prueba completado con éxito 🎉")