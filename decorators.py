import allure
import pytest
import sys

@pytest.mark.parametrize("input,expected", [(1,2), (3,4)])
def test_add(input, expected):
    assert input + 1 == expected

# С комбинацией параметров
@pytest.mark.parametrize("x", [1,2])
@pytest.mark.parametrize("y", [3,4])
def test_multiple(x, y):
    print(x, y)  # Запустится 4 раза

@pytest.mark.skip(reason="Не реализовано")
def test_feature():
    pass

# Условный пропуск
@pytest.mark.skipif(sys.version_info < (3,8), reason="Требуется Python 3.8+")
def test_python_version():
    pass

@pytest.mark.xfail(reason="Баг еще не исправлен")
def test_buggy():
    assert 1 == 2  # Тест упадет, но будет помечен как xfail

@pytest.mark.xfail(raises=ZeroDivisionError)
def test_division():
    1/0  # Ожидаем конкретное исключение

@pytest.mark.timeout(5)  # Тест должен выполниться за 5 секунд
def test_fast_operation():
    pass

@pytest.mark.asyncio # Для асинхронных тестов
async def test_async_function():
    result = await async_operation()
    assert result is not None

# Комбинированные декораторы
@pytest.mark.slow
@pytest.mark.parametrize("n", [10, 100, 1000])
@pytest.mark.skipif(not HAS_NUMPY, reason="NumPy не установлен")
def test_large_computation(n):
    """Тест с множественными декораторами"""
    assert compute(n) > 0

def pytest_configure(config):
    """Регистрация кастомного маркера"""
    config.addinivalue_line("markers", "repeat(n): запустить тест n раз")

@pytest.mark.repeat(5)
def test_random_behavior():
    """Запустится 5 раз"""
    pass

@pytest.mark.parametrize("user", [
    pytest.param(User("admin"), id="admin_user"),
    pytest.param(User("guest"), id="guest_user"),
    pytest.param(User(""), marks=pytest.mark.xfail, id="empty_user"),
])
def test_user_roles(user):
    assert user.has_permission()


@allure.feature("Авторизация")
@pytest.mark.regression
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "correct", True),
    ("admin", "wrong", False),
    pytest.param("", "", False, marks=pytest.mark.xfail),
])
def test_login(username, password, expected, database):
    """Комплексный тест логина"""
    result = database.login(username, password)
    assert result == expected

