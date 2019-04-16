import schema
from sqlalchemy import create_engine

engine = create_engine('sqlite:///rockart.db')
schema.metadata.create_all(engine)
