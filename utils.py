import json

def retrieve_phone_code(driver):
    """
    Busca en los logs de red de Chrome la respuesta que contiene el código SMS.
    Retorna el código como texto.
    """
    print("🔍 Buscando código en logs de red...")
    logs = driver.get_log("performance")
    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
            if message["method"] == "Network.responseReceived":
                request_id = message["params"]["requestId"]
                response = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                body = response.get("body", "")
                if "code" in body:
                    match = json.loads(body)
                    if isinstance(match, dict) and "code" in match:
                        print(f"📬 Código extraído: {match['code']}")
                        return match["code"]
        except Exception:
            continue
    print("⚠️ No se encontró código en los logs, usando '0000' por defecto.")
    return "0000"
