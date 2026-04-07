import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

# Конфигурация
LOGIN = "-"
PASSWORD = "-"


@pytest.fixture(scope="session")
def browser():
    """Фикстура, создающая браузер один раз для всех тестов"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def auth_browser(browser):
    """Фикстура для авторизованного браузера"""
    # Используем переданный browser, НЕ вызываем его как функцию
    browser.get("https://stepik.org/lesson/236895/step/1")

    # # Пробуем найти кнопку входа (если уже авторизованы, её не будет)
    # try:
    #     # Проверяем, не авторизованы ли уже
    #     browser.find_element(By.CSS_SELECTOR, ".navbar__profile")
    #     print("✅ Уже авторизованы")
    #     return browser
    # except:
    #     pass

    # Выполняем вход
    try:
        # Нажимаем кнопку входа
        entering = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "ember501"))
        )
        entering.click()

        # Вводим логин
        name = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        name.send_keys(LOGIN)

        # Вводим пароль
        password = browser.find_element(By.NAME, "password")
        password.send_keys(PASSWORD)

        # Отправляем форму
        submit = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )
        submit.click()

        # Ждем успешного входа
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar__profile"))
        )
        print("✅ Авторизация выполнена")
        time.sleep(2)

    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
        raise

    return browser


class TestStepik:
    @pytest.mark.parametrize("link", [
        'https://stepik.org/lesson/236895/step/1',
        'https://stepik.org/lesson/236896/step/1',
        'https://stepik.org/lesson/236897/step/1',
        'https://stepik.org/lesson/236898/step/1',
        'https://stepik.org/lesson/236899/step/1',
        'https://stepik.org/lesson/236903/step/1',
        'https://stepik.org/lesson/236904/step/1',
        'https://stepik.org/lesson/236905/step/1'
    ])
    def test_send_answer(self, auth_browser, link):
        browser = auth_browser  # Просто присваиваем для удобства

        # Переходим по ссылке
        browser.get(link)

        # Ждем загрузки страницы
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        try:
            again_button = browser.find_element(By.CSS_SELECTOR, "[class='again-btn white']")
            time.sleep(2)
            again_button.click()
        except:
            pass

        try:
            ok_button = browser.find_element(By.XPATH, "//button[text()='OK']")
            time.sleep(2)
            ok_button.click()
        except:
            pass

        # Вводим ответ
        time.sleep(5)
        textarea = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "textarea[placeholder='Напишите ваш ответ здесь...']"))
        )
        textarea.send_keys(math.log(int(time.time())))

        # Отправляем ответ
        send_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "submit-submission"))
        )
        send_button.click()

        # Проверяем результат
        result = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "smart-hints__hint"))
        )
        assert result.text == "Correct!", f"Expected 'Correct!', got '{result.text}'"

        time.sleep(3)