import pytest


@pytest.fixture
def resource(request):
    print("\nSetup resource")

    def fin():
        print("\nTeardown resource (via addfinalizer)")

    request.addfinalizer(fin)

    # Здесь можно вернуть объект для теста
    return "some_resource"


def test_example(resource):
    print(f"\nUsing {resource}")
    assert resource == "some_resource"
#
# Важное отличие от yield:
# Если в фикстуре с yield возникает исключение до yield, финализатор не выполнится.
# С addfinalizer функция очистки будет вызвана в любом случае, даже если в самой
# фикстуре (до return) произошла ошибка

import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Получаем request из item (тест-кейса)
        request = item._request

        # Добавляем финализатор, который прикрепит скриншот
        def attach_screenshot():
            if hasattr(request.node, 'driver'):
                screenshot = request.node.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="screenshot_on_failure", attachment_type=allure.attachment_type.PNG)

        request.addfinalizer(attach_screenshot)