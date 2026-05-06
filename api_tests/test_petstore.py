import requests
from api_tests.config import BASE_URL


def test_criar_pet():
    payload = {
        "id": 123456,
        "name": "Tom",
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Tom"


def test_buscar_pet():
    response = requests.get(f"{BASE_URL}/pet/123456")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "id" in response.json()


def test_atualizar_pet():
    payload = {
        "id": 123456,
        "name": "Tom Atualizado",
        "status": "sold"
    }
    response = requests.put(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Tom Atualizado"


def test_deletar_pet():
    response = requests.delete(f"{BASE_URL}/pet/123456")
    assert response.status_code in [200, 404]


def test_buscar_pets_por_status():
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "available"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_criar_order():
    payload = {
        "id": 1,
        "petId": 123456,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }
    response = requests.post(f"{BASE_URL}/store/order", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "placed"


def test_buscar_order():
    response = requests.get(f"{BASE_URL}/store/order/1")
    assert response.status_code in [200, 404]


def test_deletar_order():
    response = requests.delete(f"{BASE_URL}/store/order/1")
    assert response.status_code in [200, 404]


def test_inventario():
    response = requests.get(f"{BASE_URL}/store/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_criar_usuario():
    payload = {
        "id": 99999,
        "username": "laura_test",
        "firstName": "Laura",
        "lastName": "Teste",
        "email": "laura@test.com",
        "password": "123456",
        "phone": "999999999",
        "userStatus": 1
    }
    response = requests.post(f"{BASE_URL}/user", json=payload)
    assert response.status_code == 200


def test_buscar_usuario():
    response = requests.get(f"{BASE_URL}/user/laura_test")
    assert response.status_code in [200, 404]


def test_atualizar_usuario():
    payload = {
        "id": 99999,
        "username": "laura_test",
        "firstName": "Laura Atualizada",
        "lastName": "Teste",
        "email": "laura@test.com",
        "password": "123456",
        "phone": "999999999",
        "userStatus": 1
    }
    response = requests.put(f"{BASE_URL}/user/laura_test", json=payload)
    assert response.status_code in [200, 404]


def test_deletar_usuario():
    response = requests.delete(f"{BASE_URL}/user/laura_test")
    assert response.status_code in [200, 404]