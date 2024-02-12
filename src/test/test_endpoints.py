from pytest_flask import client

def test_upload_csv(client):
    csv_data = {'file': (BytesIO(b'my_csv_data'), 'test.csv')}
    response = client.post('/upload/csv', data=csv_data)
    assert response.status_code == 200
    assert b'CSV file uploaded and processed successfully' in response.data


def test_employees_by_department_job(client):
    response = client.get('/employees_by_department_job')
    assert response.status_code == 200
    assert len(response.json) > 0


def test_departments_hiring_most(client):
    response = client.get('/hired_over_mean')
    assert response.status_code == 200
    assert len(response.json) > 0
