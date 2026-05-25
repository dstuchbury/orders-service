from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class Order(SQLModel, table=True):
    order_uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    customer_name: str
    order_date: datetime = Field(default_factory=datetime.utcnow)
    order_status: str = "pending"
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class LineItem(SQLModel, table=True):
    line_item_uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    order_uuid: UUID
    sku: str
    quantity: int
    price: float
    updated_at: datetime = Field(default_factory=datetime.utcnow)
