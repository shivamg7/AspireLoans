FROM postgres:12

# COPY init db script so that it will be execute when the postgres container is initialized for the first time
COPY create-aspire-db.sql /docker-entrypoint-initdb.d/create-db.sql