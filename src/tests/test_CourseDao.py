import pytest
from unittest.mock import MagicMock, patch
from database.CourseDao import CourseDao
from sqlalchemy.sql import text

# Mock de datos
mock_courses = [
    {"id": "1", "name": "Mathematics", "credits": 4, "beginDate": "2024-01-01"},
    {"id": "2", "name": "Physics", "credits": 3, "beginDate": "2024-02-01"},
]

# Mock de una entidad Course para pruebas de creación/actualización
class MockCourse:
    def __init__(self, id, name, credits, beginDate):
        self.id = id
        self.name = name
        self.credits = credits
        self.beginDate = beginDate


@pytest.fixture
def mock_engine(mocker):
    """Mock del motor de base de datos"""
    return mocker.patch("database.CourseDao.engine")


@pytest.fixture
def mock_connection(mock_engine):
    """Mock de la conexión"""
    connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = connection
    return connection


def test_get_all_courses(mock_connection):
    """Prueba para CourseDao.get_all_courses"""
    # Mockear el resultado esperado
    mock_result = [MagicMock(_mapping=course) for course in mock_courses]

    # Patch de la conexión al engine
    with patch("database.CourseDao.engine.connect") as mock_connect:
        # Configurar el mock para que devuelva el resultado simulado
        mock_connection = mock_connect.return_value.__enter__.return_value
        mock_connection.execute.return_value = mock_result

        # Ejecutar el método
        result = CourseDao.get_all_courses()

        # Validar que el resultado sea el esperado
        assert result == mock_courses
        mock_connection.execute.assert_called_once()


def test_get_course_by_id(mock_connection):
    """Prueba para CourseDao.get_course_by_id"""
    # Mock del resultado
    mock_connection.execute.return_value.fetchone.return_value = MagicMock(_mapping=mock_courses[0])

    # Ejecutar
    result = CourseDao.get_course_by_id("1")

    # Validar
    assert result == mock_courses[0]
    mock_connection.execute.assert_called_once()


def test_create_course(mock_connection):
    """Prueba para CourseDao.create_course"""
    # Mock del curso
    mock_course = MockCourse("3", "Chemistry", 5, "2024-03-01")
    mock_connection.execute.return_value.rowcount = 1

    # Ejecutar
    result = CourseDao.create_course(mock_course)

    # Validar
    assert result == 1
    mock_connection.execute.assert_called_once()


def test_update_course(mock_connection):
    """Prueba para CourseDao.update_course"""
    # Mock del curso
    mock_course = MockCourse("1", "Mathematics Advanced", 5, "2024-04-01")
    mock_connection.execute.return_value.rowcount = 1

    # Ejecutar
    result = CourseDao.update_course(mock_course)

    # Validar
    assert result == 1
    mock_connection.execute.assert_called_once()


def test_delete_course(mock_connection):
    """Prueba para CourseDao.delete_course"""
    mock_connection.execute.return_value.rowcount = 1

    # Ejecutar
    result = CourseDao.delete_course("1")

    # Validar
    assert result == 1
    mock_connection.execute.assert_called_once()
