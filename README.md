# SPDB-project
## Starting database
In order to run containers type:\
`docker-compose up`
## Connecting database with pgAdmin
If you want to connect pgAdmin container with PostgisContainer check current IpAddres of PostgisContainer.\
You can do this by typing:\
`docker inspect postgis_container`
## Setting up environment
Create python venv:\
`python3 -m venv path_to_your_venv`\
Activate your venv:\
`source path_to_your_venv\bin\activate`\
Install packages:\
`pip install -r requirements.txt`
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

## Run fastAPI server
First you need to go to SPDB-project/app and then call:\
`uvicorn main:app --reload`\
API will be hosted on your localhost (default port 8000).
