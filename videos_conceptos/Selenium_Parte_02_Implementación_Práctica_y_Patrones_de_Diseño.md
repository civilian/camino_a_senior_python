Saber la historia es importante, pero ¿cómo se traduce todo eso en código robusto y mantenible? Pasemos de la teoría a la práctica y veamos cómo escribir automatizaciones que no se rompan con el primer cambio en la web, usando el patrón que separa a los juniors de los seniors.

# Selenium

### 4. Implementación Práctica: Del Código a la Realidad

#### Instalación y Configuración (El modo moderno)
Olvídate de descargar manualmente los drivers. Usa una biblioteca para gestionarlos.

```bash
pip install selenium webdriver-manager
```

#### Ejemplo 1: El "Hola Mundo" de la Automatización

```python
# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Configuración moderna y automática del driver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 1. Navegar a una página
    driver.get("https://www.wikipedia.org")

    # 2. Encontrar un elemento
    search_input = driver.find_element(By.ID, "searchInput")

    # 3. Interactuar con el elemento
    search_input.send_keys("Automatización de pruebas")

    # 4. Encontrar y hacer clic en otro elemento
    search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    search_button.click()

    # 5. Verificar un resultado
    first_heading = driver.find_element(By.ID, "firstHeading")
    print(f"El título de la página es: {first_heading.text}")
    assert "Automatización de pruebas" in first_heading.text

finally:
    # Siempre cerrar el navegador
    driver.quit()
```

#### Patrones de Uso: De Junior a Senior

##### Mal vs. Bien: Esperando Elementos

El mayor error de un principiante es asumir que la web es instantánea. Las páginas tardan en cargar, los elementos aparecen con AJAX.

**El Anti-Patrón: `time.sleep()` (El Mal)**
```python
# MAL: Frágil, lento e ineficiente
import time
# ...
search_button.click()
time.sleep(5) # ¿Y si tarda 6s? ¿Y si tarda 0.1s? Has perdido 4.9s.
first_heading = driver.find_element(By.ID, "firstHeading")
```
Esto es el equivalente a cruzar una calle con los ojos cerrados y esperar 5 segundos, esperando que no venga ningún coche.

**El Patrón Correcto: Esperas Explícitas (El Bien)**
```python
# BIEN: Robusto, eficiente y claro
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ...
search_button.click()

# Espera un MÁXIMO de 10 segundos, pero continúa tan pronto como la condición se cumpla.
wait = WebDriverWait(driver, 10)
first_heading = wait.until(
    EC.presence_of_element_located((By.ID, "firstHeading"))
)
# El código continúa inmediatamente cuando el elemento aparece.
```
Esto es como esperar en un paso de peatones y cruzar en cuanto el semáforo se pone en verde. Esperas solo lo necesario.

##### Patrón Avanzado: Page Object Model (POM)

A medida que una suite de pruebas crece, mezclar la lógica de las pruebas con los localizadores de los elementos se convierte en un infierno de mantenimiento. Si un ID cambia, tienes que actualizarlo en 20 archivos de prueba diferentes. El POM resuelve esto.

> "En la programación orientada a objetos, el Page Object es un objeto de diseño que representa la interfaz de usuario de una página, o parte de ella, y las interacciones con ella." — **Martin Fowler**, *martinfowler.com*

**Estructura de archivos:**
```
tests/
|-- pages/
|   |-- __init__.py
|   |-- base_page.py
|   |-- login_page.py
|-- test_cases/
|   |-- __init__.py
|   |-- test_login.py
```

**`pages/login_page.py` (La representación de la página)**
```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Los localizadores se definen en un solo lugar
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login-btn")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://mi-app.com/login")

    def login(self, username, password):
        """ encapsula la acción de iniciar sesión """
        self.do_send_keys(self.USERNAME_INPUT, username)
        self.do_send_keys(self.PASSWORD_INPUT, password)
        self.do_click(self.LOGIN_BUTTON)
    
    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)
```
*(`base_page.py` contendría métodos de ayuda como `do_click`, `do_send_keys` que incluyen esperas explícitas)*

**`test_cases/test_login.py` (La prueba en sí)**
```python
import pytest
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver_init") # Usando un fixture de Pytest para el setup del driver
class TestLogin:
    def test_login_failed(self):
        # La prueba es declarativa y legible. No se preocupa por los IDs o CSS.
        login_p = LoginPage(self.driver)
        login_p.login("user_incorrecto", "pass_incorrecto")
        error_msg = login_p.get_error_message()
        assert "Credenciales inválidas" in error_msg
```
**¿Por qué es esto de nivel Senior?** Porque demuestra una comprensión de la mantenibilidad, la abstracción y el principio de Responsabilidad Única (SRP). La página se encarga de "cómo" interactuar, la prueba se encarga de "qué" verificar.