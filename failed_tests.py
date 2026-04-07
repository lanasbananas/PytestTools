import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.mark.parametrize('locator',["button.btn", "no_such_button.btn"])
def test_exception1(locator):

    with webdriver.Chrome() as driver:
        driver.get("https://suninjuly.github.io/registration1.html")
        with pytest.raises(NoSuchElementException):
            driver.find_element(By.CSS_SELECTOR, locator)
            pytest.fail("Не должно быть кнопки Отправить")
