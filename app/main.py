from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database.connection_psycopg2 import conn
import json

import pathfinder as pf

cursor = conn.cursor()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    cursor.execute("SELECT * FROM planet_osm_line;")
    return cursor.fetchmany(5)
    # return {"test": "Root Page"}

@app.post('/calculate-journey')
async def calculate_journey(request: Request):
    # sample_data = {
    #     'places': [
    #         {
    #             'lat': 52.215933,
    #             'lng': 19.134422,
    #             'openingTime': {'hours': 8, 'minutes': 0},
    #             'closingTime': {'hours': 20, 'minutes': 0},
    #             'visitingTime': {'hours': 2, 'minutes': 0, 'seconds': 0},
    #             'address': 'Polska'
    #         }, ...
    #     ],
    #     'transportationTypes': {
    #         'car': True,
    #         'bike': False,
    #         'foot': False
    #     },
    #     'startingTime': {'hours': 8, 'minutes': 0},
    #     'endingTime': {'hours': 8, 'minutes': 0} or None,
    #     'startingPoint': {'lat': 52.21436403584128, 'lng': 21.077957153320312}
    # }
    data = await request.json()
    print(data)

    places = data["places"]
    transport = data["transportationTypes"]
    starting_time = data["startingTime"]
    starting_point = data["startingPoint"]

    pf.find_path(cursor, starting_point, places, starting_time, transport)

    print(type(cursor))

    return {"test": "Hello World"}
