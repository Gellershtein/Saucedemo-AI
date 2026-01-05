from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

from utils.logger import log_decorator

class CartPage(BasePage):
    """
    Страница корзины.
    """
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        """
        Конструктор класса CartPage.
        :param driver: экземпляр веб-драйвера
        """
        super().__init__(driver, driver.current_url)

    @log_decorator
    @allure.step("Получить количество товаров в корзине")
    def get_items_count_in_cart(self):
        """
        Возвращает количество товаров, отображаемых в корзине.
        :return: количество товаров
        """
        return len(self.find_elements(self._CART_ITEMS))

    @log_decorator
    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        """
        Нажимает на кнопку 'Checkout'.
        """
        self.click_element(self._CHECKOUT_BUTTON)

    @log_decorator
    @allure.step("Получить названия товаров в корзине")
    def get_item_names_in_cart(self):
        """
        Возвращает список названий всех товаров в корзине.
        :return: список названий товаров
        """
        items = self.find_elements(self._CART_ITEMS)
        item_names = [item.find_element(*self._ITEM_NAME).text for item in items]
        return item_names
