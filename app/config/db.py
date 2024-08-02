from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://appuser:P4ssw0rd@mysql:3306/fastapi_app")

meta = MetaData()

conn = engine.connect()