import pytest
# Регистрация кастомных маркеров в pytest.ini:
# markers =
#     slow: медленные тесты
#     integration: интеграционные тесты
#     smoke: дымовые тесты

@pytest.mark.slow
def test_heavy_computation():
    pass

@pytest.mark.integration
@pytest.mark.smoke
def test_api():
    pass

# Запуск по маркерам:
# pytest -m "slow"          # только медленные
# pytest -m "not slow"      # все кроме медленных
# pytest -m "smoke and integration"  # комбинация
