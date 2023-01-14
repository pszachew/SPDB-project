-- Database: spdb

-- DROP DATABASE IF EXISTS spdb;

CREATE DATABASE spdb
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

\connect spdb;

CREATE EXTENSION postgis;
CREATE EXTENSION pgrouting;
