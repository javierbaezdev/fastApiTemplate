from sqlalchemy import create_engine, MetaData
from ..API.v1.constans.db import URI_BD

engine = create_engine(URI_BD)

meta = MetaData()

conn = engine.connect()