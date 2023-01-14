type sql_scripts\createdb.sql | docker exec -i pgrouting_container psql -U admin -d postgres

osm2pgsql-bin\osm2pgsql.exe -c -d spdb -U admin -W -H localhost -S osm2pgsql-bin\default.style osm_data\mazowieckie-latest.osm.pbf

type sql_scripts\preparedb.sql | docker exec -i pgrouting_container psql -U admin -d spdb