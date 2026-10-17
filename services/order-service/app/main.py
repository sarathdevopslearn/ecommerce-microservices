import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service")

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL", "http://product-service:5001"
)
INVENTORY_SERVICE_URL = os.getenv(
    "INVENTORY_SERVICE_URL", "http://inventory-service:5003"
)
PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL", "http://payment-service:5006"
)
USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL", "http://user-service:5002"
)
NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL", "http://notification-service:5005"
)


class Order(BaseModel):
    user_id: int
    username: str | None = None
    product_id: int
    quantity: int


orders = []


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}


@app.post("/orders")
def create_order(order: Order):
    if order.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # 1. Validate the user if username is provided.
    if order.username:
        try:
            response = httpx.get(
                f"{USER_SERVICE_URL}/users/{order.username}",
                timeout=5.0
            )
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=400, detail="User validation failed"
            )
        except httpx.HTTPError:
            raise HTTPException(
                status_code=502, detail="Unable to contact user service"
            )

    # 2. Fetch product details.
    try:
        response = httpx.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}",
            timeout=5.0
        )
        response.raise_for_status()
        product = response.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(
            status_code=502, detail="Product service returned an error"
        )
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502, detail="Unable to contact product service"
        )

    # 3. Check inventory.
    try:
        response = httpx.get(
            f"{INVENTORY_SERVICE_URL}/inventory/{order.product_id}",
            timeout=5.0
        )
        response.raise_for_status()
        inventory = response.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=409,
                detail="Product is not available in inventory"
            )
        raise HTTPException(
            status_code=502, detail="Inventory service returned an error"
        )
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502, detail="Unable to contact inventory service"
        )

    if inventory["quantity"] < order.quantity:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Insufficient inventory",
                "available_quantity": inventory["quantity"]
            }
        )

    # 4. Calculate order total.
    order_id = len(orders) + 1
    amount = product["price"] * order.quantity

    # 5. Create payment record.
    payment_payload = {
        "order_id": order_id,
        "user_id": order.user_id,
        "amount": amount,
        "payment_method": "upi"
    }

    try:
        response = httpx.post(
            f"{PAYMENT_SERVICE_URL}/payments",
            json=payment_payload,
            timeout=5.0
        )
        response.raise_for_status()
        payment = response.json()
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502, detail="Payment service request failed"
        )

    # 6. Create order notification.
    notification_payload = {
        "user_id": order.user_id,
        "message": (
            f"Order {order_id} created for {product['name']}. "
            f"Total: {amount} INR. "
            f"Payment status: {payment.get('status', 'unknown')}."
        ),
        "type": "order_created"
    }

    try:
        response = httpx.post(
            f"{NOTIFICATION_SERVICE_URL}/notifications",
            json=notification_payload,
            timeout=5.0
        )
        response.raise_for_status()
        notification = response.json()
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502, detail="Notification service request failed"
        )

    # 7. Return the order and dependent-service responses.
    new_order = {
        "order_id": order_id,
        "user_id": order.user_id,
        "username": order.username,
        "product_id": order.product_id,
        "product": product,
        "quantity": order.quantity,
        "total_amount": amount,
        "status": "created",
        "inventory": inventory,
        "payment": payment,
        "notification": notification
    }

    orders.append(new_order)
    return new_order


@app.get("/orders")
def get_orders():
    return orders
