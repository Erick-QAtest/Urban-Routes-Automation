import json
import time
from selenium.common.exceptions import WebDriverException

def retrieve_phone_code(driver):
    """
    Busca en los logs de red de Chrome la respuesta que contiene el código SMS.
    Retorna el código como texto. Si no lo encuentra, devuelve "0000" por defecto.
    """
    for _ in range(10):  # intenta varias veces
        try:
            logs = driver.get_log("performance")
            for log_entry in reversed(logs):
                if "message" in log_entry:
                    message = json.loads(log_entry["message"])["message"]
                    url = message.get("params", {}).get("request", {}).get("url", "")
                    if "api/v1/number?number" in url:
                        request_id = message["params"]["requestId"]
                        body = driver.execute_cdp_cmd(
                            "Network.getResponseBody", {"requestId": request_id}
                        )
                        if body and "body" in body and isinstance(body["body"], str):
                            code = "".join([c for c in body["body"] if c.isdigit()])
                            if code:
                                return code
        except WebDriverException:
            time.sleep(1)
        except json.JSONDecodeError:
            continue
    # fallback seguro
    return "0000"
