FROM bitnami/postgresql:16

USER root

# Install build dependencies
RUN apt-get update -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false || true && \
    apt-get install -y wget build-essential lsb-release libpq-dev \
    liblz4-dev zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add PostgreSQL repository
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL development files
RUN apt-get update -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false || true && \
    apt-get install -y postgresql-server-dev-16 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and compile pg_repack
RUN wget https://github.com/reorg/pg_repack/archive/ver_1.5.0.tar.gz && \
    tar xzf ver_1.5.0.tar.gz && \
    cd pg_repack-ver_1.5.0 && \
    make && \
    make install && \
    cd .. && \
    rm -rf pg_repack-ver_1.5.0 ver_1.5.0.tar.gz

# Set the library path
ENV LD_LIBRARY_PATH /opt/bitnami/postgresql/lib:$LD_LIBRARY_PATH

USER 1001


