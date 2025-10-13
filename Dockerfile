FROM ubuntu:22.04

# Installer MySQL et Python
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server python3 python3-pip && \
    pip3 install flask mysql-connector-python

# Copier ton application et le dump SQL
WORKDIR /app
COPY . /app
COPY init_db.sql /init_db.sql

# Initialiser la base de données au démarrage
RUN service mysql start && \
    mysql -e "CREATE DATABASE IF NOT EXISTS docker_bdd;" && \
    mysql docker_bdd < /init_db.sql

# Exposer les ports Flask et MySQL
EXPOSE 5000 3306

# Lancer MySQL et Flask ensemble
CMD service mysql start && python3 app.py