from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URI = 'postgresql://admin:password@postgis_db:5432/spdb'

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
