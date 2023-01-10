from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Session
from database.connection_psycopg2 import conn
import models

cursor = conn.cursor()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

local_session = Session()

@app.get('/')
def root():
    cursor.execute("SELECT * FROM geometries;")
    return cursor.fetchall()


@app.post('/calculate-journey')
async def calculate_journey(request: Request):
    data = await request.json()
    print(data)
    return {"test": "Hello World"}
