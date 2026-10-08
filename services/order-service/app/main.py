from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service")


class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int


orders = []


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}


@app.post("/orders")
def create_order(order: Order):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    new_order = {
        "order_id": len(orders) + 1,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "created",
    }

    orders.append(new_order)

    return new_order


@app.get("/orders")
def get_orders():
    return orders