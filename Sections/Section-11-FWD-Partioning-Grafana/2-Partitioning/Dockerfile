FROM postgres:16

# Install dependencies
RUN apt-get update && apt-get install -y make git build-essential

# Clone pg_partman repository
RUN mkdir /temp && cd /temp && \
    git clone https://github.com/pgpartman/pg_partman

# Build and install pg_partman
WORKDIR /temp/pg_partman
RUN make NO_BGW=1 install

# Clean up
RUN apt-get remove -y make git build-essential && \
    rm -rf /var/lib/apt/lists/* /temp

# Copy any additional scripts or configurations if needed
# COPY scripts/ /docker-entrypoint-initdb.d/

CMD ["postgres"]
