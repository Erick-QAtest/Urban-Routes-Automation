# Project: Automation – Urban Routes  

## Project Description  

This project contains a suite of automated tests for the **Urban Routes** web application.  
The main goal is to simulate the complete user journey when requesting a taxi — from setting origin and destination to confirming the final order, including:  

- Selecting Comfort tariff.  
- Adding and confirming a phone number with SMS code.  
- Adding a credit card for payment.  
- Sending a message to the driver.  
- Selecting extra options (blanket & tissues).  
- Adding ice creams to the order.  
- Confirming the final taxi request.  

The tests validate **critical flows** to guarantee a smooth, stable, and error-free user experience.  

---

## Technologies and Techniques Used  

* **Python 3.x** – Core language for scripts.  
* **Selenium WebDriver** – Browser automation engine.  
* **Pytest** – Framework for test execution and reporting.  
* **Page Object Model (POM)** – Clean separation of locators/actions vs. test logic.  
* **Explicit Waits** (`WebDriverWait`, `ExpectedConditions`) – Ensures stability against dynamic elements.  
* **JavaScript Execution** – For cases where elements are overlapped (e.g., overlays, tricky sliders).  
* **Performance Log Interception** – Used to capture network responses and retrieve SMS confirmation codes.  
* **Safe Click Helpers** – Custom logic to handle overlays and intercepted clicks reliably.  

---

## Project Structure  

qa-project-Urban-Routes-es/
├── .venv/ # Virtual environment
├── data.py # Test data (URLs, addresses, phone, card, etc.)
├── test_urban_routes.py # Main test suite (Pytest)
├── urban_routes_page.py # Page Object Model implementation
├── utils.py # Helper utilities (e.g., retrieve SMS code from logs)
└── README.md # This documentation



---

## Setup and Execution  

### 1. Requirements  

Make sure you have installed:  
* **Python 3.8+** (recommended: latest stable)  
* **pip** package manager  

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
Your requirements.txt should include:

nginx
Copiar código
selenium
pytest
webdriver-manager
(Optional for reporting & parallel runs):

css
Copiar código
pytest-html
pytest-xdist
4. Configure Test Data
Edit data.py with safe test values:

python
Copiar código
# data.py
urban_routes_url = "https://your-urban-routes-url"
address_from = "East 2nd Street, 601"
address_to = "1300 1st St"
phone_number = "+1 123 456 7890"
card_number = "4242 4242 4242 4242"
card_cvv = "123"
⚠️ Use test data only — never real card numbers or personal data.

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
Generate a test report (optional):

bash
Copiar código
pytest --html=report.html --self-contained-html
Run in parallel (optional):

bash
Copiar código
pytest -n auto
6. Deactivate Virtual Environment
bash
Copiar código
deactivate
go
Copiar código
