from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from .....config.db import engine, meta

usersTable = Table("users", meta,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), nullable=False),
    Column("password", String(50), nullable=False),
    Column("email", String(50), nullable=False, unique=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False)
)

meta.create_all(engine)

