import pytest
import allure
from faker import Faker

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage, CheckoutUserData
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.checkout_complete_page import CheckoutCompletePage

fake = Faker()

@allure.feature("SauceDemo E2E")
class TestSauceDemo:
    
    @allure.story("Успешный вход в систему")
    @allure.title("Тест успешного входа в систему")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        """
        Тест проверяет успешный вход в систему с валидными данными.
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        with allure.step("Выполнить вход с валидными данными"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Проверить, что открылась страница каталога"):
            assert inventory_page.is_inventory_page_open(), "Страница каталога не открылась"

    @allure.story("Работа с корзиной")
    @allure.title("Тест добавления товара в корзину")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_item_to_cart(self, driver):
        """
        Тест проверяет добавление товара в корзину.
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)

        with allure.step("Выполнить вход"):
            login_page.login("standard_user", "secret_sauce")
        
        with allure.step("Добавить первый товар в корзину"):
            inventory_page.add_item_to_cart_by_index(0)

        with allure.step("Перейти в корзину"):
            inventory_page.go_to_cart()

        with allure.step("Проверить, что в корзине один товар"):
            assert cart_page.get_items_count_in_cart() == 1, "Количество товаров в корзине неверное"

    @allure.story("Оформление заказа")
    @allure.title("Тест полного цикла оформления заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_checkout_process(self, driver):
        """
        Тест проверяет полный цикл оформления заказа от начала до конца.
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_one_page = CheckoutStepOnePage(driver)
        checkout_two_page = CheckoutStepTwoPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)

        with allure.step("Выполнить вход"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Добавить товар в корзину"):
            inventory_page.add_item_to_cart_by_index(0)

        with allure.step("Перейти в корзину"):
            inventory_page.go_to_cart()

        with allure.step("Перейти к оформлению заказа"):
            cart_page.proceed_to_checkout()

        with allure.step("Заполнить данные пользователя"):
            user_data = CheckoutUserData(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                postal_code=fake.zipcode()
            )
            checkout_one_page.fill_user_information(user_data)
        
        with allure.step("Продолжить оформление"):
            checkout_one_page.click_continue()

        with allure.step("Проверить, что открылась страница обзора"):
            assert checkout_two_page.is_overview_page_open(), "Не открылась страница обзора заказа"
        
        with allure.step("Завершить заказ"):
            checkout_two_page.click_finish()

        with allure.step("Проверить сообщение об успешном заказе"):
            assert "Thank you for your order!" in checkout_complete_page.get_complete_message(), \
                "Сообщение о завершении заказа неверное"

    @allure.story("Вход в систему с ошибкой")
    @allure.title("Тест входа с неверными кредами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login(self, driver):
        """
        Тест проверяет, что при вводе неверных данных появляется сообщение об ошибке.
        """
        login_page = LoginPage(driver)

        with allure.step("Выполнить вход с невалидными данными"):
            login_page.login("wrong_user", "wrong_password")

        with allure.step("Проверить сообщение об ошибке"):
            expected_error = "Epic sadface: Username and password do not match any user in this service"
            assert expected_error in login_page.get_error_message(), "Сообщение об ошибке неверное"

