import psycopg2

conn = psycopg2.connect(
    host="pgrouting_container",
    database="spdb",
    user="admin",
    port=5432,
    password="password")
