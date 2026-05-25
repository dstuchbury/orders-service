from sqlmodel import Session, select
from sqlalchemy import func
from app.models import Order, LineItem
from app.schemas import OrderCreate


def create_order(session: Session, order_in: OrderCreate):
    order = Order(customer_name=order_in.customer_name)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order(session: Session, order_uuid):
    statement = select(Order).where(Order.order_uuid == order_uuid)
    return session.exec(statement).first()


def get_orders_paginated(session: Session, page: int, page_size: int):
    # Count total rows
    total = session.exec(select(func.count()).select_from(Order)).one()

    # Pagination math
    offset = (page - 1) * page_size

    # Fetch rows
    orders = session.exec(
        select(Order).order_by(Order.order_date.desc()).offset(offset).limit(page_size)
    ).all()

    return orders, total


def create_line_item(session: Session, item: LineItem):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_line_items_for_order(session: Session, order_uuid, page: int, page_size: int):
    total = session.exec(
        select(func.count()).select_from(LineItem).where(LineItem.order_uuid == order_uuid)
    ).one()

    # Pagination math
    offset = (page - 1) * page_size

    # Fetch rows
    line_items = session.exec(
        select(LineItem)
        .where(LineItem.order_uuid == order_uuid)
        .offset(offset)
        .limit(page_size)
    ).all()

    return line_items, total
