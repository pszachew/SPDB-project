-- how to use dijkstra pgrouting
SELECT * FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM tb_roads_noded', 1, 9, false);

-- get distance between two geometries
SELECT ST_Distance(a.the_geom, b.the_geom)
from tb_roads_noded_vertices_pgr a, tb_roads_noded_vertices_pgr b
where a.id = 1 and b.id = 5;

