from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///data/property.db')
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
