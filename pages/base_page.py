from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

from utils.logger import log_decorator

class BasePage:
    """
    Базовый класс для всех страниц. Содержит общие методы для взаимодействия с элементами.
    """
    
    def __init__(self, driver, url):
        """
        Конструктор класса BasePage.
        :param driver: экземпляр веб-драйвера
        :param url: URL-адрес страницы
        """
        self.driver = driver
        self.url = url

    @log_decorator
    @allure.step("Открыть страницу")
    def open(self):
        """
        Открывает URL страницы в браузере.
        """
        self.driver.get(self.url)

    @log_decorator
    @allure.step("Найти видимый элемент {locator}")
    def find_element(self, locator, time=10):
        """
        Находит один видимый элемент на странице.
        :param locator: кортеж (By, 'selector')
        :param time: время ожидания элемента в секундах
        :return: найденный веб-элемент
        :raises: TimeoutException если элемент не найден
        """
        try:
            return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_on_error", attachment_type=allure.attachment_type.PNG)
            raise

    @log_decorator
    @allure.step("Найти все видимые элементы {locator}")
    def find_elements(self, locator, time=10):
        """
        Находит все видимые элементы на странице.
        :param locator: кортеж (By, 'selector')
        :param time: время ожидания элементов в секундах
        :return: список найденных веб-элементов
        :raises: TimeoutException если элементы не найдены
        """
        try:
            return WebDriverWait(self.driver, time).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot_on_error", attachment_type=allure.attachment_type.PNG)
            raise

    @log_decorator
    @allure.step("Кликнуть по элементу {locator}")
    def click_element(self, locator, time=10):
        """
        Находит и кликает по элементу.
        :param locator: кортеж (By, 'selector')
        :param time: время ожидания элемента в секундах
        """
        element = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator))
        element.click()

    @log_decorator
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def enter_text(self, locator, text, time=10):
        """
        Находит элемент и вводит в него текст.
        :param locator: кортеж (By, 'selector')
        :param text: текст для ввода
        :param time: время ожидания элемента в секундах
        """
        element = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    @log_decorator
    @allure.step("Получить текст из элемента {locator}")
    def get_text(self, locator, time=10):
        """
        Находит элемент и возвращает его текст.
        :param locator: кортеж (By, 'selector')
        :param time: время ожидания элемента в секундах
        :return: текст элемента
        """
        element = self.find_element(locator, time)
        return element.text

    @log_decorator
    @allure.step("Кликнуть по элементу {locator} с помощью JavaScript")
    def js_click_element(self, locator, time=10):
        """
        Находит и кликает по элементу с помощью JavaScript.
        :param locator: кортеж (By, 'selector')
        :param time: время ожидания элемента в секундах
        """
        element = self.find_element(locator, time)
        self.driver.execute_script("arguments[0].click();", element)
