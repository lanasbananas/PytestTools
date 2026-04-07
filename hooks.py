# @pytest.hookimpl — это декоратор в pytest, который позволяет вам встраивать свой код
# в процесс выполнения тестов. Простыми словами: вы говорите pytest:
# "Когда дойдешь до определенного этапа (например, перед запуском теста), выполни мою функцию".

import pytest

@pytest.hookimpl
def pytest_runtest_setup(item):
    """Выполняется перед каждым тестом"""
    print(f"\n🔥 Сейчас начнется тест: {item.name}")

@pytest.hookimpl
def pytest_runtest_teardown(item):
    """Выполняется после каждого теста"""
    print(f"✅ Тест {item.name} завершен")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    """Этот код выполнится раньше всех других обработчиков"""
    print("Я самый первый!")

@pytest.hookimpl(trylast=True)
def pytest_runtest_call(item):
    """Этот код выполнится позже всех"""
    print("Я подведу итоги...")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    print("🟢 ДО выполнения теста")

    yield  # Здесь pytest выполняет сам тест

    print("🔴 ПОСЛЕ выполнения теста")


# Порядок выполнения (важно!)
# Когда несколько хуков одного типа, они выполняются в таком порядке:
#
# Сначала все hookwrapper=True (но доходят только до yield)
#
# Потом все с tryfirst=True
#
# Затем остальные в порядке, обратном загрузке
#
# После всех с trylast=True
#
# В конце возвращаемся к hookwrapper и выполняем код после yield