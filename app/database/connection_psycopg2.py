import psycopg2

conn = psycopg2.connect(
    host="postgis_db",
    database="spdb",
    user="admin",
    port=5432,
    password="password")
