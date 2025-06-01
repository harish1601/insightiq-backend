from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from models.order import Order
from models.user import User
from database.database import get_db
from utils.auth import get_current_user
from io import StringIO
import datetime

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))

    required_columns = {"order_date", "product", "category", "quantity", "price", "total"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail="CSV missing required columns")

    for _, row in df.iterrows():
        order = Order(
            order_date=datetime.datetime.strptime(row["order_date"], "%Y-%m-%d").date(),
            product=row["product"],
            category=row["category"],
            quantity=int(row["quantity"]),
            price=float(row["price"]),
            total=float(row["total"]),
            user_id=current_user.id
        )
        db.add(order)

    db.commit()
    return {"message": "Orders uploaded successfully"}