def test_category_management_requires_admin(client, admin_headers, user_headers):
    payload = {"name": "Books", "slug": "books", "description": "Printed books"}
    assert client.post("/categories/", json=payload).status_code == 401
    assert client.post("/categories/", json=payload, headers=user_headers).status_code == 403
    response = client.post("/categories/", json=payload, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["description"] == "Printed books"


def test_order_rejects_bad_quantities_and_updates_stock_atomically(client, admin_headers, user_headers):
    category = client.post("/categories/", json={"name": "Books", "slug": "books"}, headers=admin_headers).json()
    product = client.post("/products/", json={"name": "Book", "price": "12.50", "stock": 3, "category_id": category["id"]}, headers=admin_headers)
    assert product.status_code == 201
    pid = product.json()["id"]
    assert client.post("/orders/", json={"items": [{"product_id": pid, "quantity": -1}]}, headers=user_headers).status_code == 422
    failed = client.post("/orders/", json={"items": [{"product_id": pid, "quantity": 4}]}, headers=user_headers)
    assert failed.status_code == 400
    assert client.get(f"/products/{pid}").json()["stock"] == 3
    success = client.post("/orders/", json={"items": [{"product_id": pid, "quantity": 2}]}, headers=user_headers)
    assert success.status_code == 201
    assert success.json()["total_price"] == "25.00"
    assert client.get(f"/products/{pid}").json()["stock"] == 1
    order_id = success.json()["id"]
    assert client.get(f"/orders/{order_id}", headers=user_headers).status_code == 200
    client.post("/auth/register", json={"email": "other@example.com", "password": "test-password"})
    other_token = client.post("/auth/login", data={"username": "other@example.com", "password": "test-password"}).json()["access_token"]
    assert client.get(f"/orders/{order_id}", headers={"Authorization": f"Bearer {other_token}"}).status_code == 404


def test_product_update_and_delete_are_admin_only(client, admin_headers, user_headers):
    category = client.post("/categories/", json={"name": "Books", "slug": "books"}, headers=admin_headers).json()
    payload = {"name": "Book", "price": "12.50", "stock": 3, "category_id": category["id"]}
    product = client.post("/products/", json=payload, headers=admin_headers).json()
    payload["price"] = "9.99"
    assert client.put(f"/products/{product['id']}", json=payload, headers=user_headers).status_code == 403
    updated = client.put(f"/products/{product['id']}", json=payload, headers=admin_headers)
    assert updated.status_code == 200
    assert updated.json()["price"] == "9.99"
    assert client.delete(f"/products/{product['id']}", headers=admin_headers).status_code == 204
