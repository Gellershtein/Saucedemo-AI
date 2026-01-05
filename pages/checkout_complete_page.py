from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

from utils.logger import log_decorator

class CheckoutCompletePage(BasePage):
    """
    Страница успешного завершения заказа.
    """
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        """
        Конструктор класса CheckoutCompletePage.
        :param driver: экземпляр веб-драйвера
        """
        super().__init__(driver, driver.current_url)

    @log_decorator
    @allure.step("Получить сообщение о завершении заказа")
    def get_complete_message(self):
        """
        Возвращает текст заголовка об успешном оформлении заказа.
        :return: текст сообщения
        """
        return self.get_text(self._COMPLETE_HEADER)
