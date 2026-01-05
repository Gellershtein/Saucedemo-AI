from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

from utils.logger import log_decorator

class InventoryPage(BasePage):
    """
    Страница с каталогом товаров.
    """
    _ADD_TO_CART_BUTTON = (By.XPATH, "//button[text()='Add to cart']")
    _CART_ICON = (By.ID, "shopping_cart_container")
    _PAGE_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        """
        Конструктор класса InventoryPage.
        :param driver: экземпляр веб-драйвера
        """
        super().__init__(driver, driver.current_url)

    @log_decorator
    @allure.step("Проверить, что страница каталога открыта")
    def is_inventory_page_open(self):
        """
        Проверяет, что страница каталога открыта, по наличию заголовка.
        :return: True, если страница открыта, иначе False
        """
        return "Products" in self.get_text(self._PAGE_TITLE)

    @log_decorator
    @allure.step("Добавить товар в корзину по индексу: {index}")
    def add_item_to_cart_by_index(self, index=0):
        """
        Добавляет товар в корзину, выбирая его по индексу.
        :param index: индекс товара на странице (начиная с 0)
        """
        add_buttons = self.find_elements(self._ADD_TO_CART_BUTTON)
        if index < len(add_buttons):
            add_buttons[index].click()
        else:
            raise IndexError("Индекс товара выходит за пределы диапазона")

    @log_decorator
    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """
        Нажимает на иконку корзины для перехода на страницу корзины.
        """
        self.click_element(self._CART_ICON)
