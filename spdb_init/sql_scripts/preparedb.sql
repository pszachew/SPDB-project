-- prepare database

-- coordinates: long_W = 20.5321 , lat_N = 52.3945, long_E = 21.6101 , lat_S = 52.0233
-- extract rectangle which contains Warsaw

-- temporary table with warsaw coords
create table warsaw_polygon as
select ST_Polygon('LINESTRING(20.5321 52.3945, 21.6101 52.3945, 21.6101 52.0233, 20.5321 52.0233, 20.5321 52.3945)'::geometry, 4326) as polygon;

-- prepare raw point table to operate on geographical coordinates
alter table planet_osm_point add point_gcord Geometry(Point, 4326);

-- **********************************
-- create production table - tb_point
-- **********************************
update planet_osm_point
set point_gcord = ST_Transform(way, 4326);

create table tb_points as 
select 
osm_id, access, "addr:housename", "addr:housenumber", amenity, barrier, bicycle, brand,
building, capital, construction, denomination, foot, highway, historic, junction, leisure,
man_made, name, "natural", office, operator, place, population, public_transport, railway,
religion, service, shop, sport, surface, tourism, way, point_gcord
-- ST_X(way) as x, ST_Y(way) as y, ST_X(point_gcord) as long, ST_Y(point_gcord) as lat -- do testow
from planet_osm_point t1, warsaw_polygon t2
where ST_Contains(t2.polygon, t1.point_gcord);
-- ST_X(point_gcord) > 20.5321 and ST_X(point_gcord) < 21.6101 and ST_Y(point_gcord) > 52.0233 and ST_Y(point_gcord) < 52.3945


-- **********************************
-- create production table - tb_roads
-- **********************************
alter table planet_osm_roads 
add line_gcord Geometry(LineString, 4326),
add line_centroid Geometry(Point, 4326);

alter table planet_osm_roads
rename column way to line_ccord;

update planet_osm_roads
set line_centroid=ST_Centroid(ST_Transform(line_ccord, 4326)),
line_gcord = ST_Transform(line_ccord, 4326);

create table tb_roads as
select
-- general information
osm_id as id, bicycle, bridge, boundary, foot, highway, junction, name, oneway, operator, railway, service, surface, 
-- geometry types
line_ccord, line_gcord as the_geom, line_centroid
from planet_osm_roads as t1, (select * from warsaw_polygon) as wp
where ST_Within(t1.line_gcord, wp.polygon)=true 
or ST_Intersects(wp.polygon, t1.line_gcord);


-- create network from roads 
-- tabname: tb_roads_noded
select pgr_nodeNetwork('tb_roads', 0.00001);

-- create topology 
-- tabname: tb_roads_noded_vertices_pgr
select pgr_createTopology('tb_roads_noded', 0.00001);


ALTER TABLE tb_roads_noded ADD COLUMN name VARCHAR, ADD COLUMN type VARCHAR;

UPDATE tb_roads_noded AS new SET name=old.name, type=old.highway FROM tb_roads as old
WHERE new.old_id = old.id;

ALTER TABLE tb_roads_noded ADD distance FLOAT8;

UPDATE tb_roads_noded SET distance = ST_Length(ST_Transform(the_geom, 4326)::geography) / 1000;



-- ************************************
-- create production table - tb_polygon
-- ************************************

alter table planet_osm_polygon add column polyg_gcord Geometry(POLYGON, 4326), add column polyg_centroid Geometry(POINT, 4326);

alter table planet_osm_polygon rename way to polyg_ccord;

-- Query returned successfully in 2 min 11 secs.
update planet_osm_polygon
set polyg_gcord = ST_Transform(polyg_ccord, 4326);

create table tb_polygon as
select
-- general information
osm_id as id, access, amenity, area, barrier, brand, boundary, building, denomination, highway, landuse, leisure, man_made, name, "natural", operator, 
place, population, public_transport, religion, shop, sport, surface, tourism, wetland, way_area, 
-- geometry types
polyg_ccord, polyg_gcord, polyg_centroid
from planet_osm_polygon as t1, (select * from warsaw_polygon) as wp
where ST_Within(t1.polyg_gcord, wp.polygon)=true 
or ST_Intersects(wp.polygon, t1.polyg_gcord);

update tb_polygon
set polyg_centroid=ST_Centroid(polyg_gcord);


-- ************************************
-- create production table - tb_line
-- ************************************

alter table planet_osm_line 
add line_gcord Geometry(LineString, 4326),
add line_centroid Geometry(Point, 4326);

alter table planet_osm_line
rename column way to line_ccord;

update planet_osm_line
set line_gcord = ST_Transform(line_ccord, 4326);

create table tb_line as
select
-- general information
osm_id as id, bicycle, bridge, boundary, foot, highway, junction, name, oneway, operator, railway, service, surface, 
-- geometry types
line_ccord, line_gcord, line_centroid
from planet_osm_line as t1, (select * from warsaw_polygon) as wp
where ST_Within(t1.line_gcord, wp.polygon)=true 
or ST_Intersects(wp.polygon, t1.line_gcord);

update tb_line
set line_centroid=ST_Centroid(line_gcord);


-- FUNCTIONS

CREATE OR REPLACE FUNCTION closest_points(long FLOAT8, lat FLOAT8) 
    RETURNS TABLE (
		vid BIGINT
) 
AS $$
BEGIN
    RETURN QUERY SELECT
		tab.id
    FROM
		(
			SELECT
		 		ST_Distance(
					t1.the_geom, 
					ST_SetSRID(ST_MakePoint(long, lat), 4326))
					as distance,
				t1.id
		 	FROM tb_roads_noded_vertices_pgr t1
			ORDER BY distance
			LIMIT 10
		 ) as tab
	;
END; $$ 
LANGUAGE 'plpgsql';

-- example USAGE
-- select * from closest_points(21.03395661433369, 52.192651949999994)

