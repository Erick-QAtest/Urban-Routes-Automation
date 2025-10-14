import time
import json
from selenium.common.exceptions import WebDriverException


def retrieve_phone_code(driver, timeout=20, poll_frequency=2):
    """
    Retrieves the SMS confirmation code from Chrome performance logs.
    
    The function inspects network logs captured by the browser to find
    API requests related to phone verification, extracts digits from
    the response, and returns the last 4-digit code.

    Args:
        driver: Selenium WebDriver instance with "performance" logging enabled.
        timeout (int): Maximum wait time (in seconds) to find the code.
        poll_frequency (int): Time (in seconds) between polling attempts.

    Returns:
        str: 4-digit confirmation code.

    Raises:
        TimeoutError: If no code is found within the time limit.
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            logs = driver.get_log("performance")
            for log_entry in reversed(logs):
                message_json = log_entry.get("message")
                if not message_json:
                    continue

                try:
                    message = json.loads(message_json)["message"]
                except (json.JSONDecodeError, KeyError):
                    continue

                # Detect API request related to phone verification
                url = message.get("params", {}).get("request", {}).get("url", "")
                if "api/v1/number?number" in url:
                    request_id = message["params"]["requestId"]

                    # Retrieve response body from network log
                    response = driver.execute_cdp_cmd(
                        "Network.getResponseBody", {"requestId": request_id}
                    )

                    if response and isinstance(response.get("body"), str):
                        digits = "".join(x for x in response["body"] if x.isdigit())
                        if len(digits) >= 4:
                            code = digits[-4:]
                            print(f"📲 Confirmation code detected: {code}")
                            return code

        except WebDriverException:
            # If the driver temporarily fails to retrieve logs, retry
            pass

        time.sleep(poll_frequency)

    raise TimeoutError("❌ No confirmation code found within the timeout period.")

