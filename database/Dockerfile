FROM postgres:9.6
COPY ./sql/create_tables.sql /docker-entrypoint-initdb.d/
COPY ./sql/seed.sql /docker-entrypoint-initdb.d/
