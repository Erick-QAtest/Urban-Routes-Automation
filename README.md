# Proyecto de Automatización: Urban Routes

## Descripción del Proyecto

Este proyecto contiene un conjunto de pruebas de automatización para la aplicación web "Urban Routes". El objetivo principal es simular el flujo completo de un usuario al solicitar un taxi, desde la selección de origen y destino hasta la confirmación final del pedido, incluyendo la configuración de opciones adicionales y la gestión de pagos con tarjeta de crédito.

Las pruebas están diseñadas para verificar la funcionalidad crítica de la aplicación y asegurar una experiencia de usuario fluida y sin errores.

## Tecnologías y Técnicas Utilizadas

* **Python 3.x:** Lenguaje de programación principal utilizado para escribir los scripts de automatización.
* **Selenium WebDriver:** Framework de automatización web para interactuar con el navegador.
* **Pytest:** Framework de pruebas para estructurar y ejecutar las pruebas de manera eficiente.
* **WebDriver Manager:** Biblioteca para gestionar automáticamente los controladores del navegador (ChromeDriver en este caso), eliminando la necesidad de descargarlos y configurarlos manualmente.
* **Patrón Page Object Model (POM):** Las pruebas están organizadas utilizando el patrón POM, lo que mejora la reusabilidad del código, la legibilidad y la mantenibilidad al separar los elementos de la página y las interacciones de la lógica de las pruebas.
* **Manejo de Waits (Esperas Explícitas):** Se utilizan `WebDriverWait` con `ExpectedConditions` para manejar los elementos dinámicos de la interfaz de usuario, asegurando que los elementos estén presentes y sean interactuables antes de realizar acciones sobre ellos. Se han incluido `time.sleep()` estratégicos en puntos críticos para manejar transiciones o cargas asíncronas cuando las esperas explícitas no eran suficientes por sí solas.
* **Intercepción de Logs de Rendimiento:** Se utiliza la capacidad de Selenium para acceder a los logs de rendimiento del navegador, lo que permite interceptar solicitudes de red y extraer datos como códigos SMS de confirmación.
* **Ejecución de JavaScript:** En algunos casos, se recurre a la ejecución de JavaScript directamente en el navegador para interactuar con elementos que pueden ser difíciles de cliquear mediante los métodos estándar de Selenium (e.g., elementos cubiertos por otros o con eventos de clic complejos).

## Estructura del Proyecto

¡Absolutamente! Un buen README.md es esencial para cualquier proyecto, especialmente uno de automatización. Aquí tienes una plantilla completa que puedes usar para tu proyecto, escrita en Markdown para que la copies directamente en tu archivo README.md.

Markdown

# Proyecto de Automatización: Urban Routes

## Descripción del Proyecto

Este proyecto contiene un conjunto de pruebas de automatización para la aplicación web "Urban Routes". El objetivo principal es simular el flujo completo de un usuario al solicitar un taxi, desde la selección de origen y destino hasta la confirmación final del pedido, incluyendo la configuración de opciones adicionales y la gestión de pagos con tarjeta de crédito.

Las pruebas están diseñadas para verificar la funcionalidad crítica de la aplicación y asegurar una experiencia de usuario fluida y sin errores.

## Tecnologías y Técnicas Utilizadas

* **Python 3.x:** Lenguaje de programación principal utilizado para escribir los scripts de automatización.
* **Selenium WebDriver:** Framework de automatización web para interactuar con el navegador.
* **Pytest:** Framework de pruebas para estructurar y ejecutar las pruebas de manera eficiente.
* **WebDriver Manager:** Biblioteca para gestionar automáticamente los controladores del navegador (ChromeDriver en este caso), eliminando la necesidad de descargarlos y configurarlos manualmente.
* **Patrón Page Object Model (POM):** Las pruebas están organizadas utilizando el patrón POM, lo que mejora la reusabilidad del código, la legibilidad y la mantenibilidad al separar los elementos de la página y las interacciones de la lógica de las pruebas.
* **Manejo de Waits (Esperas Explícitas):** Se utilizan `WebDriverWait` con `ExpectedConditions` para manejar los elementos dinámicos de la interfaz de usuario, asegurando que los elementos estén presentes y sean interactuables antes de realizar acciones sobre ellos. Se han incluido `time.sleep()` estratégicos en puntos críticos para manejar transiciones o cargas asíncronas cuando las esperas explícitas no eran suficientes por sí solas.
* **Intercepción de Logs de Rendimiento:** Se utiliza la capacidad de Selenium para acceder a los logs de rendimiento del navegador, lo que permite interceptar solicitudes de red y extraer datos como códigos SMS de confirmación.
* **Ejecución de JavaScript:** En algunos casos, se recurre a la ejecución de JavaScript directamente en el navegador para interactuar con elementos que pueden ser difíciles de cliquear mediante los métodos estándar de Selenium (e.g., elementos cubiertos por otros o con eventos de clic complejos).

## Estructura del Proyecto

qa-project-Urban-Routes-es/
├── .venv/                      # Entorno virtual de Python
├── data.py                     # Archivo para almacenar datos de prueba (URL, credenciales, etc.)
├── main.py                     # Script para ejecutar la prueba manualmente (opcional)
├── test_urban_routes.py        # Archivo principal de las pruebas de Pytest
├── urban_routes_page.py        # Implementación del Page Object Model
└── utils.py                    # Funciones de utilidad (ej. para extraer códigos del log)
└── README.md                   # Este archivo


## Instrucciones para Ejecutar las Pruebas

Sigue estos pasos para configurar y ejecutar las pruebas de automatización en tu entorno local:

### 1. Requisitos Previos

Asegúrate de tener instalado:

* **Python 3.8+** (preferiblemente la última versión estable)
* **pip** (gestor de paquetes de Python)

### 2. Configuración del Entorno Virtual

Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
# Navega al directorio raíz de tu proyecto
cd /path/to/your/qa-project-Urban-Routes-es

# Crea un entorno virtual (si aún no existe)
python3 -m venv .venv

# Activa el entorno virtual
# En macOS/Linux:
source .venv/bin/activate
# En Windows (CMD):
.venv\Scripts\activate.bat
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
3. Instalación de Dependencias
Una vez activado el entorno virtual, instala las bibliotecas necesarias:

Bash

pip install selenium pytest webdriver-manager

4. Configuración de Datos de Prueba
Edita el archivo data.py en el directorio raíz de tu proyecto para incluir los datos necesarios para las pruebas, como la URL de la aplicación, direcciones, números de teléfono de prueba, detalles de tarjeta de crédito (si son de prueba/seguros):

Python
# data.py
urban_routes_url = "[https://tu-url-de-la-aplicacion-urban-routes.com](https://tu-url-de-la-aplicacion-urban-routes.com)" # ¡Reemplaza con la URL real!
address_from = "East 2nd Street, 601"
address_to = "1300 1st St"
phone_number = "+11234567890" # Asegúrate de que este número sea válido para recibir SMS de prueba
card_number = "1234 5678 9012 3456" # Usa un número de tarjeta de prueba seguro
card_cvv = "123" # Usa un CVV de prueba seguro
Asegúrate de usar datos de prueba válidos y seguros. Nunca uses datos reales de tarjetas de crédito o información personal sensible.

5. Ejecutar las Pruebas
Con el entorno virtual activado, puedes ejecutar las pruebas utilizando Pytest desde el directorio raíz del proyecto:

Bash

pytest
Para ver la salida detallada de print() durante la ejecución (útil para el debugging):

Bash
pytest -s

Para ejecutar una prueba específica:

Bash
pytest test_urban_routes.py::TestUrbanRoutes::test_full_order

6. Desactivar el Entorno Virtual
Cuando hayas terminado de trabajar con el proyecto, puedes desactivar el entorno virtual:

Bash

deactivate
# Proyecto de Automatización: Urban Routes

## Descripción del Proyecto

Este proyecto contiene un conjunto de pruebas de automatización para la aplicación web "Urban Routes". El objetivo principal es simular el flujo completo de un usuario al solicitar un taxi, desde la selección de origen y destino hasta la confirmación final del pedido, incluyendo la configuración de opciones adicionales y la gestión de pagos con tarjeta de crédito.

Las pruebas están diseñadas para verificar la funcionalidad crítica de la aplicación y asegurar una experiencia de usuario fluida y sin errores.

## Tecnologías y Técnicas Utilizadas

* **Python 3.x:** Lenguaje de programación principal utilizado para escribir los scripts de automatización.
* **Selenium WebDriver:** Framework de automatización web para interactuar con el navegador.
* **Pytest:** Framework de pruebas para estructurar y ejecutar las pruebas de manera eficiente.
* **WebDriver Manager:** Biblioteca para gestionar automáticamente los controladores del navegador (ChromeDriver en este caso), eliminando la necesidad de descargarlos y configurarlos manualmente.
* **Patrón Page Object Model (POM):** Las pruebas están organizadas utilizando el patrón POM, lo que mejora la reusabilidad del código, la legibilidad y la mantenibilidad al separar los elementos de la página y las interacciones de la lógica de las pruebas.
* **Manejo de Waits (Esperas Explícitas):** Se utilizan `WebDriverWait` con `ExpectedConditions` para manejar los elementos dinámicos de la interfaz de usuario, asegurando que los elementos estén presentes y sean interactuables antes de realizar acciones sobre ellos. Se han incluido `time.sleep()` estratégicos en puntos críticos para manejar transiciones o cargas asíncronas cuando las esperas explícitas no eran suficientes por sí solas.
* **Intercepción de Logs de Rendimiento:** Se utiliza la capacidad de Selenium para acceder a los logs de rendimiento del navegador, lo que permite interceptar solicitudes de red y extraer datos como códigos SMS de confirmación.
* **Ejecución de JavaScript:** En algunos casos, se recurre a la ejecución de JavaScript directamente en el navegador para interactuar con elementos que pueden ser difíciles de cliquear mediante los métodos estándar de Selenium (e.g., elementos cubiertos por otros o con eventos de clic complejos).

## Estructura del Proyecto

¡Absolutamente! Un buen README.md es esencial para cualquier proyecto, especialmente uno de automatización. Aquí tienes una plantilla completa que puedes usar para tu proyecto, escrita en Markdown para que la copies directamente en tu archivo README.md.

Markdown

# Proyecto de Automatización: Urban Routes

## Descripción del Proyecto

Este proyecto contiene un conjunto de pruebas de automatización para la aplicación web "Urban Routes". El objetivo principal es simular el flujo completo de un usuario al solicitar un taxi, desde la selección de origen y destino hasta la confirmación final del pedido, incluyendo la configuración de opciones adicionales y la gestión de pagos con tarjeta de crédito.

Las pruebas están diseñadas para verificar la funcionalidad crítica de la aplicación y asegurar una experiencia de usuario fluida y sin errores.

## Tecnologías y Técnicas Utilizadas

* **Python 3.x:** Lenguaje de programación principal utilizado para escribir los scripts de automatización.
* **Selenium WebDriver:** Framework de automatización web para interactuar con el navegador.
* **Pytest:** Framework de pruebas para estructurar y ejecutar las pruebas de manera eficiente.
* **WebDriver Manager:** Biblioteca para gestionar automáticamente los controladores del navegador (ChromeDriver en este caso), eliminando la necesidad de descargarlos y configurarlos manualmente.
* **Patrón Page Object Model (POM):** Las pruebas están organizadas utilizando el patrón POM, lo que mejora la reusabilidad del código, la legibilidad y la mantenibilidad al separar los elementos de la página y las interacciones de la lógica de las pruebas.
* **Manejo de Waits (Esperas Explícitas):** Se utilizan `WebDriverWait` con `ExpectedConditions` para manejar los elementos dinámicos de la interfaz de usuario, asegurando que los elementos estén presentes y sean interactuables antes de realizar acciones sobre ellos. Se han incluido `time.sleep()` estratégicos en puntos críticos para manejar transiciones o cargas asíncronas cuando las esperas explícitas no eran suficientes por sí solas.
* **Intercepción de Logs de Rendimiento:** Se utiliza la capacidad de Selenium para acceder a los logs de rendimiento del navegador, lo que permite interceptar solicitudes de red y extraer datos como códigos SMS de confirmación.
* **Ejecución de JavaScript:** En algunos casos, se recurre a la ejecución de JavaScript directamente en el navegador para interactuar con elementos que pueden ser difíciles de cliquear mediante los métodos estándar de Selenium (e.g., elementos cubiertos por otros o con eventos de clic complejos).

## Estructura del Proyecto

qa-project-Urban-Routes-es/
├── .venv/                      # Entorno virtual de Python
├── data.py                     # Archivo para almacenar datos de prueba (URL, credenciales, etc.)
├── main.py                     # Script para ejecutar la prueba manualmente (opcional)
├── test_urban_routes.py        # Archivo principal de las pruebas de Pytest
├── urban_routes_page.py        # Implementación del Page Object Model
└── utils.py                    # Funciones de utilidad (ej. para extraer códigos del log)
└── README.md                   # Este archivo


## Instrucciones para Ejecutar las Pruebas

Sigue estos pasos para configurar y ejecutar las pruebas de automatización en tu entorno local:

### 1. Requisitos Previos

Asegúrate de tener instalado:

* **Python 3.8+** (preferiblemente la última versión estable)
* **pip** (gestor de paquetes de Python)

### 2. Configuración del Entorno Virtual

Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
# Navega al directorio raíz de tu proyecto
cd /path/to/your/qa-project-Urban-Routes-es

# Crea un entorno virtual (si aún no existe)
python3 -m venv .venv

# Activa el entorno virtual
# En macOS/Linux:
source .venv/bin/activate
# En Windows (CMD):
.venv\Scripts\activate.bat
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
3. Instalación de Dependencias
Una vez activado el entorno virtual, instala las bibliotecas necesarias:

Bash

pip install selenium pytest webdriver-manager

4. Configuración de Datos de Prueba
Edita el archivo data.py en el directorio raíz de tu proyecto para incluir los datos necesarios para las pruebas, como la URL de la aplicación, direcciones, números de teléfono de prueba, detalles de tarjeta de crédito (si son de prueba/seguros):

Python
# data.py
urban_routes_url = "[https://tu-url-de-la-aplicacion-urban-routes.com](https://tu-url-de-la-aplicacion-urban-routes.com)" # ¡Reemplaza con la URL real!
address_from = "East 2nd Street, 601"
address_to = "1300 1st St"
phone_number = "+11234567890" # Asegúrate de que este número sea válido para recibir SMS de prueba
card_number = "1234 5678 9012 3456" # Usa un número de tarjeta de prueba seguro
card_cvv = "123" # Usa un CVV de prueba seguro
Asegúrate de usar datos de prueba válidos y seguros. Nunca uses datos reales de tarjetas de crédito o información personal sensible.

5. Ejecutar las Pruebas
Con el entorno virtual activado, puedes ejecutar las pruebas utilizando Pytest desde el directorio raíz del proyecto:

Bash

pytest
Para ver la salida detallada de print() durante la ejecución (útil para el debugging):

Bash
pytest -s

Para ejecutar una prueba específica:

Bash
pytest test_urban_routes.py::TestUrbanRoutes::test_full_order

6. Desactivar el Entorno Virtual
Cuando hayas terminado de trabajar con el proyecto, puedes desactivar el entorno virtual:

Bash

deactivate
