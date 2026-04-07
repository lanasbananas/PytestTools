import pytest

@pytest.fixture
def database():
    """Подготовка данных"""
    db = create_db()
    yield db  # Тест использует db
    db.close()  # Очистка после теста

@pytest.fixture(scope="session")  # Один раз на всю сессию
def global_config():
    return {"url": "http://example.com"}

@pytest.fixture(autouse=True)  # Автоматически применяется ко всем тестам
def setup_logging():
    setup_logs()
    yield
    cleanup_logs()


@pytest.mark.usefixtures("database", "cache")
class TestUserAPI:
    """Фикстуры применяются ко всем тестам класса"""

    def test_create_user(self):
        pass

    @pytest.mark.parametrize("role", ["admin", "user"])
    def test_permissions(self, role):
        pass