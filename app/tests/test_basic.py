import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    return app.test_client()

def test_test_route(client):
    response = client.get('/test')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Test route works!' 