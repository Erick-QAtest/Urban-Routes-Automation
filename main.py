import time
import data
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from urban_routes_page import UrbanRoutesPage

def retrieve_phone_code(driver) -> str:
    code = None
    for _ in range(10):
        try:
            logs = [log["message"] for log in driver.get_log("performance") if log.get("message") and "api/v1/number?number" in log["message"]]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": message_data["params"]["requestId"]})
                code = ''.join([x for x in body["body"] if x.isdigit()])
                if code:
                    return code
        except WebDriverException:
            time.sleep(1)
    raise Exception("❌ No se encontró el código de confirmación del teléfono.")

def main():
    print("🚀 Iniciando prueba manual Urban Routes...")
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(driver)

        page.set_from(data.address_from)
        page.set_to(data.address_to)
        page.click_request_taxi()
        page.select_comfort()
        page.send_phone_number(data.phone_number)

        print("⌛ Esperando para interceptar el código...")
        time.sleep(2)
        code = retrieve_phone_code(driver)
        page.confirm_sms_code(code)

        page.add_credit_card(data.card_number, data.card_cvv)
        page.write_message("Gracias por pasar por mí")
        page.toggle_blanket_and_tissues()
        page.add_ice_cream()
        page.wait_for_final_modal()

        print("✅ Flujo completado con éxito 🎉")
    finally:
        print("🧹 Cerrando navegador")
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()