from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from .....config.db import engine, meta
from ...helpers.mixin import TimestampMixin, DeletedMixin


acceptedTermsTable = Table("accepted_terms", meta,
    Column("id", Integer, primary_key=True),
    Column("description", String(500), nullable=False),
    *TimestampMixin.get_columns(),
    *DeletedMixin.get_columns(),

    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)

rolesTable = Table("roles", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    *TimestampMixin.get_columns(),
    *DeletedMixin.get_columns(),
)

usersTable = Table("users", meta,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(60), nullable=False),
    Column("password", String(500), nullable=False),
    Column("email", String(50), nullable=False, unique=True),
    Column("phone", String(50), nullable=False),
    *TimestampMixin.get_columns(),
    *DeletedMixin.get_columns(),

    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False)
)

meta.create_all(engine)

