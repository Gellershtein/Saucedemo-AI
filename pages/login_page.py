from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

from utils.logger import log_decorator

class LoginPage(BasePage):
    """
    Страница аутентификации.
    """
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        """
        Конструктор класса LoginPage.
        :param driver: экземпляр веб-драйвера
        """
        super().__init__(driver, "https://www.saucedemo.com/")

    @log_decorator
    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username):
        """
        Вводит имя пользователя в соответствующее поле.
        :param username: имя пользователя
        """
        self.enter_text(self._USERNAME_INPUT, username)

    @log_decorator
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        """
        Вводит пароль в соответствующее поле.
        :param password: пароль
        """
        self.enter_text(self._PASSWORD_INPUT, password)

    @log_decorator
    @allure.step("Нажать кнопку 'Login'")
    def click_login_button(self):
        """
        Нажимает на кнопку входа.
        """
        self.click_element(self._LOGIN_BUTTON)

    @log_decorator
    @allure.step("Выполнить вход с именем пользователя '{username}'")
    def login(self, username, password):
        """
        Выполняет полный процесс входа в систему.
        :param username: имя пользователя
        :param password: пароль
        """
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    @log_decorator
    @allure.step("Получить текст ошибки")
    def get_error_message(self):
        """
        Возвращает текст сообщения об ошибке.
        :return: текст ошибки
        """
        return self.get_text(self._ERROR_MESSAGE)
