"""Small API smoke tests. Run from backend after installing requirements: pytest."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_diffraction_shape_and_limits():
    response = client.post('/api/simulate/diffraction', json={'wavelength_nm': 550, 'slit_width_um': 50, 'screen_distance_m': 1, 'points': 101})
    assert response.status_code == 200
    data = response.json()
    assert len(data['x_mm']) == 101
    assert len(data['intensity']) == 101
    assert abs(data['intensity'][50] - 1) < 1e-8

def test_integration_converges():
    coarse = client.post('/api/simulate/integration', json={'points': 11}).json()
    fine = client.post('/api/simulate/integration', json={'points': 101}).json()
    assert fine['absolute_error'] < coarse['absolute_error']

def test_out_of_range_rejected():
    response = client.post('/api/simulate/diffraction', json={'wavelength_nm': 900, 'slit_width_um': 50, 'screen_distance_m': 1, 'points': 101})
    assert response.status_code == 422
