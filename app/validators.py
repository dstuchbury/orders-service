# app/validators.py

from typing import Type
from sqlmodel import SQLModel, Session, select

from app.errors import AppValidationError


def validate_unique(
    session: Session,
    model: Type[SQLModel],
    field_name: str,
    value: object,
    message: str | None = None,
):
    field = getattr(model, field_name)

    existing = session.exec(
        select(model).where(field == value)
    ).first()

    if existing:
        readable_field = field_name.replace("_", " ")
        raise AppValidationError(
            errors={
                field_name: [
                    message or f"The {readable_field} has already been taken."
                ]
            }
        )