import pytest
import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Конфигурация
class Config:
    """Класс для хранения конфигурационных данных"""
    LOGIN = "-"
    PASSWORD = "-"
    BASE_URL = "https://stepik.org"
    TIMEOUT = 10
    SHORT_TIMEOUT = 5
    LESSONS = [
        'https://stepik.org/lesson/236895/step/1',
        'https://stepik.org/lesson/236896/step/1',
        'https://stepik.org/lesson/236897/step/1',
        'https://stepik.org/lesson/236898/step/1',
        'https://stepik.org/lesson/236899/step/1',
        'https://stepik.org/lesson/236903/step/1',
        'https://stepik.org/lesson/236904/step/1',
        'https://stepik.org/lesson/236905/step/1'
    ]


@pytest.fixture(scope="session")
def browser():
    """Фикстура, создающая браузер один раз для всех тестов"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(Config.TIMEOUT)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def auth_browser(browser):
    """Фикстура для авторизованного браузера"""
    browser.get(f"{Config.BASE_URL}/lesson/236895/step/1")

    # Проверяем, авторизованы ли уже
    if _is_logged_in(browser):
        print("✅ Уже авторизованы")
        return browser

    # Выполняем вход
    _perform_login(browser)
    return browser


def _is_logged_in(browser):
    """Проверяет, авторизован ли пользователь"""
    try:
        browser.find_element(By.CSS_SELECTOR, ".navbar__profile")
        return True
    except NoSuchElementException:
        return False


def _perform_login(browser):
    """Выполняет процесс авторизации"""
    try:
        # Нажимаем кнопку входа
        login_button = WebDriverWait(browser, Config.TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "ember501"))
        )
        login_button.click()

        # Вводим логин и пароль
        username_field = WebDriverWait(browser, Config.TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        username_field.send_keys(Config.LOGIN)

        password_field = browser.find_element(By.NAME, "password")
        password_field.send_keys(Config.PASSWORD)

        # Отправляем форму
        submit_button = WebDriverWait(browser, Config.TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="submit"]'))
        )
        submit_button.click()

        # Ждем успешного входа
        WebDriverWait(browser, Config.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar__profile"))
        )
        print("✅ Авторизация выполнена")
        time.sleep(2)

    except TimeoutException as e:
        raise TimeoutException(f"❌ Ошибка авторизации: таймаут при ожидании элемента") from e
    except Exception as e:
        raise Exception(f"❌ Ошибка авторизации: {e}") from e


def _close_modal_windows(browser):
    """Закрывает модальные окна, если они появляются"""
    modal_buttons = [
        (By.CSS_SELECTOR, "[class='again-btn white']", "кнопка 'Again'"),
        (By.XPATH, "//button[text()='OK']", "кнопка 'OK'")
    ]

    for by, selector, button_name in modal_buttons:
        try:
            button = WebDriverWait(browser, Config.SHORT_TIMEOUT).until(
                EC.element_to_be_clickable((by, selector))
            )
            button.click()
            time.sleep(1)
            print(f"✅ Закрыто модальное окно с {button_name}")
        except TimeoutException:
            continue


def _calculate_answer():
    """Вычисляет ответ для отправки"""
    return math.log(int(time.time()))


def _send_answer(browser, answer):
    """Отправляет ответ в текстовое поле"""
    textarea = WebDriverWait(browser, Config.SHORT_TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          "textarea[placeholder='Напишите ваш ответ здесь...']"))
    )
    textarea.clear()
    textarea.send_keys(str(answer))


def _submit_and_verify(browser):
    """Отправляет ответ и проверяет результат"""
    # Отправляем ответ
    send_button = WebDriverWait(browser, Config.SHORT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit-submission"))
    )
    send_button.click()

    # Проверяем результат
    result_element = WebDriverWait(browser, Config.SHORT_TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "smart-hints__hint"))
    )

    return result_element.text


class TestStepik:
    """Тестовый класс для проверки ответов на Stepik"""

    @pytest.mark.parametrize("lesson_url", Config.LESSONS)
    def test_send_answer(self, auth_browser, lesson_url):
        """
        Тест отправки ответа на уроке Stepik
        Проверяет, что ответ отправлен успешно и получен правильный результат
        """
        browser = auth_browser

        # Переходим на страницу урока
        browser.get(lesson_url)

        # Ждем загрузки страницы
        WebDriverWait(browser, Config.TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Закрываем возможные модальные окна
        _close_modal_windows(browser)

        # Вычисляем и отправляем ответ
        answer = _calculate_answer()
        _send_answer(browser, answer)

        # Отправляем и проверяем результат
        result_text = _submit_and_verify(browser)

        # Проверяем, что ответ правильный
        assert result_text == "Correct!", \
            f"Ожидался ответ 'Correct!', получен '{result_text}' для урока {lesson_url}"

        print(f"✅ Урок {lesson_url}: ответ '{answer}' отправлен успешно")
        time.sleep(2)


if __name__ == "__main__":
    # Для запуска тестов используйте команду:
    # pytest -v task_answer.py
    pass