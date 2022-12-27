from fastapi import FastAPI
from database.connection import Base, engine, Session
import models
from database.connection_psycopg2 import conn

cursor = conn.cursor()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

local_session = Session()

@app.get('/')
def root():
    cursor.execute("SELECT * FROM geometries;")
    return cursor.fetchall()