# Project: Automation – Urban Routes  

## Project Description  

This project contains a set of automated tests for the "Urban Routes" web application.  
The main goal is to simulate the complete user flow when requesting a taxi — from selecting origin and destination to the final order confirmation, including additional options and payment with a credit card.  

The tests are designed to verify critical application functionality and ensure a smooth, error-free user experience.  

## Technologies and Techniques Used  

* **Python 3.x:** Main programming language used to write automation scripts.  
* **Selenium WebDriver:** Web automation framework to interact with the browser.  
* **Pytest:** Testing framework used to structure and execute tests efficiently.  
* **WebDriver Manager:** Library to automatically manage browser drivers (e.g., ChromeDriver).  
* **Page Object Model (POM):** The tests are structured with POM, improving reusability, readability, and maintainability by separating page elements and interactions from test logic.  
* **Explicit Waits:** `WebDriverWait` with `ExpectedConditions` is used to handle dynamic elements, ensuring elements are present and interactable before performing actions. Strategic `time.sleep()` calls are included at critical points for asynchronous transitions.  
* **Performance Log Interception:** Selenium’s ability to access browser performance logs is used to intercept network requests and extract data such as SMS confirmation codes.  
* **JavaScript Execution:** In some cases, direct JavaScript execution is used to interact with tricky elements (e.g., covered or non-standard clickable elements).  

## Project Structure  

qa-project-Urban-Routes-es/
├── .venv/ # Python virtual environment
├── data.py # Test data (URLs, phone numbers, card info, etc.)
├── test_urban_routes.py # Main test suite (Pytest)
├── urban_routes_page.py # Page Object Model implementation
├── utils.py # Utility functions (e.g., SMS code retrieval)
└── README.md # This documentation

bash
Copiar código

## Setup and Execution  

### 1. Requirements  

Make sure you have installed:  
* **Python 3.8+** (latest stable recommended)  
* **pip** (Python package manager)  

### 2. Create Virtual Environment  

```bash
cd /path/to/qa-project-Urban-Routes-es
python3 -m venv .venv
Activate the environment:

macOS/Linux:

bash
Copiar código
source .venv/bin/activate
Windows (CMD):

cmd
Copiar código
.venv\Scripts\activate.bat
Windows (PowerShell):

powershell
Copiar código
.venv\Scripts\Activate.ps1
3. Install Dependencies
bash
Copiar código
pip install -r requirements.txt
requirements.txt should include:

nginx
Copiar código
selenium
pytest
webdriver-manager
4. Configure Test Data
Edit data.py with your test values:

python
Copiar código
# data.py
urban_routes_url = "https://your-urban-routes-url"
address_from = "East 2nd Street, 601"
address_to = "1300 1st St"
phone_number = "+1 123 456 7890"
card_number = "4242 4242 4242 4242"
card_cvv = "123"
⚠ Use safe test data only — never real card numbers or personal info.

5. Run Tests
Run all tests:

bash
Copiar código
pytest -v
Run with debug prints:

bash
Copiar código
pytest -s
Run a specific test:

bash
Copiar código
pytest test_urban_routes.py::TestUrbanRoutes::test_add_card
6. Deactivate Virtual Environment
bash
Copiar código
deactivate