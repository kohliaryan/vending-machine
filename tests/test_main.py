from starlette.testclient import TestClient
from main import app

def test_item_lifecycle():
    with TestClient(app) as client:
        payload = {
            "name": "Test Soda",
            "quantity": 25,
            "price": 40
        }

        # CREATE
        response = client.post("/item", json=payload)
        assert response.status_code == 201

        created_item = response.json()
        test_item_id = created_item["id"]

        assert created_item["name"] == "Test Soda"
        assert created_item["quantity"] == 25
        assert created_item["price"] == 40

        # READ
        response = client.get("/items")
        all_items = response.json()
        assert isinstance(all_items, list)

        found = False

        for item in all_items:
            if item["id"] == test_item_id:
                found = True
                assert item["quantity"] == 25
                assert item["price"] == 40
                break

        assert found == True

        # UPDATE
        response = client.post(f"/items/{test_item_id}/buy", json={"amount_paid": 10})
        assert response.status_code == 400
        assert response.json() == {'detail': 'Item is more expensive then input amount'}

        response = client.post(f"/items/{test_item_id}/buy", json={"amount_paid": 100})
        assert response.status_code == 200
        assert response.json()["change"] == 60

        response = client.put(f"/item/{test_item_id}", json={"quantity": 1})
        assert response.status_code == 200
        assert response.json()["quantity"]== 1

        response = client.delete(f"/item/{test_item_id}")
        assert response.status_code == 200

