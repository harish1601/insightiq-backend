from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.order import Order
from models.user import User
from database.database import get_db
from utils.auth import get_current_user

router = APIRouter()

@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    revenue = sum(order.total for order in user_orders)
    orders = len(user_orders)
    customers = len(set(order.id for order in user_orders))  # Simulate unique customers

    return {
        "revenue": revenue,
        "orders": orders,
        "customers": customers
    }