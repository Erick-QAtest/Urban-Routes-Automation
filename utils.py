import time
import json
from selenium.common.exceptions import WebDriverException


def retrieve_phone_code(driver, timeout=20, poll_frequency=2):
    """
    Recupera el código de confirmación del teléfono desde los logs de rendimiento del navegador.

    :param driver: instancia de Selenium WebDriver con logging habilitado ("performance").
    :param timeout: tiempo máximo en segundos para esperar el código.
    :param poll_frequency: intervalo de segundos entre intentos.
    :return: string con el código encontrado.
    :raises Exception: si no se encuentra ningún código en el tiempo límite.
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            logs = driver.get_log("performance")
            for log_entry in reversed(logs):
                if "message" not in log_entry:
                    continue

                try:
                    message = json.loads(log_entry["message"])["message"]
                except json.JSONDecodeError:
                    continue

                url = message.get("params", {}).get("request", {}).get("url", "")
                if "api/v1/number?number" in url:
                    request_id = message["params"]["requestId"]
                    body = driver.execute_cdp_cmd(
                        "Network.getResponseBody", {"requestId": request_id}
                    )

                    if body and isinstance(body.get("body"), str):
                        digits = "".join(x for x in body["body"] if x.isdigit())
                        if digits:
                            # Se asume que el código es de 4 dígitos
                            code = digits[-4:]
                            print(f"📲 Código de confirmación encontrado: {code}")
                            return code
        except WebDriverException:
            pass

        time.sleep(poll_frequency)

    raise Exception("❌ No se encontró el código de confirmación del teléfono en el tiempo límite.")
