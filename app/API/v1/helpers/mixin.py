from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func

class TimestampMixin:
    @classmethod
    def get_columns(cls):
        return [
            Column("created_at", DateTime, nullable=False, default=func.now()),
            Column("updated_at", DateTime, nullable=False, default=func.now(), onupdate=func.now())
        ]

class DeletedMixin:
    @classmethod
    def get_columns(cls):
        return [
            Column("is_deleted", Boolean, nullable=False, default=False)
        ]
