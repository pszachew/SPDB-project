import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="spdb",
    user="admin",
    port=5432,
    password="password")
