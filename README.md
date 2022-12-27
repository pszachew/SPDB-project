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
