# Database Security

## Enabling TLS/SSL in Postgres

```bash
# docker run
docker run --name pg -p 5432:5432 -e POSTGRES_PASSWORD=password postgres

# run pgadmin --
docker run -e PGADMIN_DEFAULT_EMAIL="smk@minetest.in" -e PGADMIN_DEFAULT_PASSWORD="password" -p 5555:80 --name pgadmin dpage/pgadmin4

# connect and pass the host as ip
docker inspect pg # get ip for connection
```

```bash
docker exec -it pg bash

# install vim
apt-get update && apt-get install vim

cd /var/lib/postgresql

# edit postgresql.conf
# edit, turn ssl = on
# create cert file, and key file & specify
openssl req -x509 -newkey rsa:4096 -nodes -keyout private.pem -out cert.pem

chmod 600 private.pem
chown postgres private.pem

docker stop pg
docker start pg
```

