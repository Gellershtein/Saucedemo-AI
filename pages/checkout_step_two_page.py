from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

from utils.logger import log_decorator

class CheckoutStepTwoPage(BasePage):
    """
    Страница второго шага оформления заказа (обзор и подтверждение).
    """
    _FINISH_BUTTON = (By.ID, "finish")
    _PAGE_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        """
        Конструктор класса CheckoutStepTwoPage.
        :param driver: экземпляр веб-драйвера
        """
        super().__init__(driver, driver.current_url)

    @log_decorator
    @allure.step("Проверить, что страница обзора заказа открыта")
    def is_overview_page_open(self):
        """
        Проверяет, что страница обзора заказа открыта.
        :return: True, если страница открыта, иначе False
        """
        return "Checkout: Overview" in self.get_text(self._PAGE_TITLE)

    @log_decorator
    @allure.step("Завершить оформление заказа")
    def click_finish(self):
        """
        Нажимает на кнопку 'Finish'.
        """
        self.js_click_element(self._FINISH_BUTTON)
