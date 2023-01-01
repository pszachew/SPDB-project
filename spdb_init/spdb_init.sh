cat sql_scripts/createdb.sql | docker exec -i pgrouting_container psql -U admin -d admin

osm2pgsql -c -d spdb -U admin -W -H localhost osm_data/mazowieckie-latest.osm.pbf
