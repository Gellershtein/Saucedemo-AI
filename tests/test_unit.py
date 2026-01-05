import pytest
from pydantic import ValidationError

from pages.checkout_step_one_page import CheckoutUserData

@pytest.mark.unit
def test_checkout_user_data_valid():
    """
    Тест проверяет успешное создание модели с валидными данными.
    """
    data = {"first_name": "John", "last_name": "Doe", "postal_code": "12345"}
    try:
        instance = CheckoutUserData(**data)
        assert instance.first_name == "John"
        assert instance.last_name == "Doe"
        assert instance.postal_code == "12345"
    except ValidationError:
        pytest.fail("Не должно быть ошибки валидации при корректных данных")

@pytest.mark.unit
@pytest.mark.parametrize("invalid_data, expected_error_part", [
    ({"last_name": "Doe", "postal_code": "12345"}, "first_name"),  # first_name отсутствует
    ({"first_name": "John", "postal_code": "12345"}, "last_name"),   # last_name отсутствует
    ({"first_name": "John", "last_name": "Doe"}, "postal_code"),      # postal_code отсутствует
    ({"first_name": "", "last_name": "Doe", "postal_code": "12345"}, "first_name"), # first_name пустой
])
def test_checkout_user_data_invalid(invalid_data, expected_error_part):
    """
    Тест проверяет, что модель данных выбрасывает исключение ValidationError
    при отсутствии обязательных полей или при некорректных значениях.
    """
    with pytest.raises(ValidationError) as exc_info:
        CheckoutUserData(**invalid_data)
    
    # Проверяем, что в тексте ошибки упоминается нужное поле
    assert expected_error_part in str(exc_info.value)
