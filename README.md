# SPDB-project
## Connecting database with pgAdmin
If you want to connect pgAdmin container with PostgisContainer check current IpAddres of PostgisContainer.\
You can do this by typing:\
`docker inspect postgis_container`
## Create spdb and load data
Download data (mazowieckie-latest.osm.pbf) from https://download.geofabrik.de/europe/poland/mazowieckie.html \
Put file to spdb_init/osm_data directory\
On Windows:\
Open command line in spdb_init folder and run:\
`spdb_init.bat`\
On Linux:\
Install osm2pgsql with command:\
`apt install osm2pgsql`\
Then open terminal in spdb_init catalog and run:\
`spdb_init.sh`\
After loading data we can uninstall osm2pgsql:\

## Run Application
In order to run containers:\
`docker-compose up --build`
