import pytest
import json
from app import app

@pytest.fixture
def client():
    """Crear cliente de prueb para Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test 1: Verificar que la página principal carga correctamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"CI/CD Pipeline" in response.data
    assert b"David Cocha" in response.data

def test_home_contains_features(client):
    """Test 2: Verificar que muestra las características"""
    response = client.get('/')
    assert b"GitHub Actions" in response.data
    assert b"Docker" in response.data
    assert b"cocha:1.0.5" in response.data

def test_home_contains_subdomain(client):
    """Test 3: Verificar que muestra el subdominio correcto"""
    response = client.get('/')
    assert b"pgcocha.byronrm.com" in response.data

def test_health_endpoint(client):
    """Test 4: Verificar el endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['version'] == '1.0.5'
    assert data['student'] == 'David Cocha'

def test_ask_endpoint_without_data(client):
    """Test 5: Verificar que el endpoint /ask requiere datos"""
    response = client.post('/ask', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400

def test_ask_endpoint_with_question(client):
    """Test 6: Verificar que el endpoint /ask responde correctamente"""
    response = client.post('/ask',
                          data=json.dumps({'question': 'Hola'}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'response' in data

def test_home_has_html_structure(client):
    """Test 7: Verificar estructura HTML básica"""
    response = client.get('/')
    assert b"<!DOCTYPE html>" in response.data
    assert b"<html" in response.data
    assert b"</html>" in response.data

def test_health_returns_json(client):
    """Test 8: Verificar que /health retorna JSON válido"""
    response = client.get('/health')
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'status' in data