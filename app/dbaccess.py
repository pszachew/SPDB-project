import psycopg2
from database.connection_psycopg2 import conn

class DbAccess:
    
    cursor = conn.cursor()
    def __init__(self, cur) -> None:
        pass

    def get_closest_point(long: float, lat: float):
        # returns table
        # id
        DbAccess.cursor.execute("SELECT * FROM closest_points({long}, {lat})".format(long=long, lat=lat))
        return DbAccess.cursor.fetchone()

    def get_shortest_path(source, target):
        # returns table
        # seq | path_seq | node | edge | cost | agg_cost
        DbAccess.cursor.execute("SELECT * FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM tb_roads_noded', {source_id}, {target_id}, false)".format(source_id=source, target_id=target))
        return DbAccess.cursor.fetchall()