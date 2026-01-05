from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pydantic import BaseModel, Field
import allure

from utils.logger import log_decorator

class CheckoutUserData(BaseModel):
    """
    Модель данных для валидации информации о пользователе при чекауте.
    """
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1)

class CheckoutStepOnePage(BasePage):
    """
    Страница первого шага оформления заказа (ввод данных пользователя).
    """
    _FIRST_NAME_INPUT = (By.ID, "first-name")
    _LAST_NAME_INPUT = (By.ID, "last-name")
    _POSTAL_CODE_INPUT = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")

    def __init__(self, driver):
        """
        Конструктор класса CheckoutStepOnePage.
        :param driver: экземпляр веб-драйвера
        """
        super().__init__(driver, driver.current_url)

    @log_decorator
    @allure.step("Заполнить информацию о пользователе: {user_data}")
    def fill_user_information(self, user_data: CheckoutUserData):
        """
        Заполняет форму с данными пользователя.
        :param user_data: Pydantic модель с данными пользователя
        """
        # Валидация данных перед использованием
        validated_data = CheckoutUserData(**user_data.model_dump())
        
        self.enter_text(self._FIRST_NAME_INPUT, validated_data.first_name)
        self.enter_text(self._LAST_NAME_INPUT, validated_data.last_name)
        self.enter_text(self._POSTAL_CODE_INPUT, validated_data.postal_code)

    @log_decorator
    @allure.step("Отправить форму с данными пользователя")
    def click_continue(self):
        """
        Отправляет форму, симулируя нажатие на 'Continue'.
        Вместо клика используется submit() для большей надежности.
        """
        self.find_element(self._POSTAL_CODE_INPUT).submit()
