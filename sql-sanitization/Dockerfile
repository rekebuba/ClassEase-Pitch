FROM google/cloud-sdk:slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY scrub.sh /scrub.sh

RUN chmod +x /scrub.sh

ENTRYPOINT ["/bin/bash", "/scrub.sh"]
