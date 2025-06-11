FROM mysql:8.0

# Copy initialization scripts
COPY init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh


HEALTHCHECK --interval=5s --timeout=10s --retries=5 \
    CMD mysqladmin ping -h localhost
