from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session
from uuid import UUID
from math import ceil

from app.db import init_db, get_session
from app.schemas import PaginatedOrders, OrderRead, OrderCreate, PaginatedLineItems
from app.models import LineItem
from app import crud

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/orders", response_model=OrderRead)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    new_order = crud.create_order(session, order)
    return new_order


@app.get("/orders", response_model=PaginatedOrders)
def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    orders, total = crud.get_orders_paginated(session, page, page_size)

    total_pages = max(1, ceil(total / page_size))

    return PaginatedOrders(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        next_page=page + 1 if page < total_pages else None,
        prev_page=page - 1 if page > 1 else None,
        orders=orders,
    )


@app.get("/orders/{order_uuid}", response_model=OrderRead)
def get_order(order_uuid: UUID, session: Session = Depends(get_session)):
    order = crud.get_order(session, order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/orders/{order_uuid}/line-items")
def create_line_item(
    order_uuid: UUID, item: LineItem, session: Session = Depends(get_session)
):
    item.order_uuid = order_uuid
    return crud.create_line_item(session, item)


@app.get("/orders/{order_uuid}/line-items", response_model=PaginatedLineItems)
def list_line_items(
    order_uuid: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    line_items, total = crud.get_line_items_for_order(session, order_uuid, page, page_size)

    total_pages = max(1, ceil(total / page_size))

    return PaginatedLineItems(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        next_page=page + 1 if page < total_pages else None,
        prev_page=page - 1 if page > 1 else None,
        items=line_items,
    )
