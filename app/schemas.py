from typing import List, Optional
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime


class OrderCreate(SQLModel):
    customer_name: str


class OrderRead(SQLModel):
    order_uuid: UUID
    customer_name: str
    order_date: datetime
    order_status: str
    updated_at: datetime


class PaginatedOrders(SQLModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    next_page: Optional[int]
    prev_page: Optional[int]
    orders: List[OrderRead]


class LineItemCreate(SQLModel):
    order_uuid: UUID
    sku: str
    quantity: int
    price: float


class LineItemRead(SQLModel):
    line_item_uuid: UUID
    order_uuid: UUID
    sku: str
    quantity: int
    price: float
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PaginatedLineItems(SQLModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    next_page: Optional[int]
    prev_page: Optional[int]
    items: List[LineItemRead]
