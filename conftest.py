import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для создания и закрытия экземпляра веб-драйвера.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Используем webdriver_manager для автоматической установки драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для добавления скриншота в отчет Allure при падении теста.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(driver.get_screenshot_as_png(),
                          name='screenshot_on_failure',
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

