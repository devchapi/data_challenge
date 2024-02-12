import pytest
from src.utils.processing import upload_to_database, execute_employees_by_department_job_service, execute_hired_over_mean_service
@pytest.fixture
def sample_data():
    data = [
        {'id': 1, 'name': 'John Doe', 'hire_date': '2024-01-01', 'department_id': 1, 'job_id': 1},
        {'id': 2, 'name': 'Jhon Doe', 'hire_date': '2024-02-02', 'department_id': 2, 'job_id': 2},
    ]
    return data

def test_upload_to_database(sample_data):
    filename = 'test.csv'  # Provide a filename for test data
    entity = 'hired_employees'  # Provide the entity for test data
    upload_to_database(filename, entity)
    
    
def test_execute_employees_by_department_job_service():
    query = "SELECT * FROM employees"
    result = execute_employees_by_department_job_service(query)
    
def test_execute_hired_over_mean_service():
    query = "SELECT * FROM hired_employees"
    result = execute_hired_over_mean_service(query)
    