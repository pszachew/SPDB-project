import psycopg2
from database.connection_psycopg2 import conn

class DbAccess:
    
    cursor = conn.cursor()
    def __init__(self, cur) -> None:
        pass

    @staticmethod
    def get_closest_point(long: float, lat: float):
        # returns table
        # id
        DbAccess.cursor.execute("SELECT * FROM closest_points({long}, {lat})".format(long=long, lat=lat))
        return DbAccess.cursor.fetchone()

    @staticmethod
    def get_shortest_path(source, target):
        # returns table
        # seq | path_seq | node | edge | cost | agg_cost
        DbAccess.cursor.execute("SELECT * FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM tb_roads_noded', {source_id}, {target_id}, false)".format(source_id=source, target_id=target))
        return DbAccess.cursor.fetchall()

    @staticmethod
    def get_path(nodes):
        where_condition = "in ("
        for i in range(len(nodes)):
            where_condition += str(nodes[i])
            if i != len(nodes)-1:
                where_condition += ","
            else:
                where_condition += ")"
        DbAccess.cursor.execute(
            "select id, st_asgeojson(the_geom) from tb_roads_noded_vertices_pgr where id {cond}"
            .format(cond=where_condition))
        return DbAccess.cursor.fetchall()