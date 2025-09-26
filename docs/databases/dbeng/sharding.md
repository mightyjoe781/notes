# Sharding

### What is sharding ?

![](assets/Pasted%20image%2020250925234921.png)

- partition table row based but put those partition into a different *database instance*.
- which database server has *SFTOJ* ? Consistent Hashing (Ownership Problem). We don't query all shards

### Consistent Hashing

![](assets/Pasted%20image%2020250925235248.png)

Consistent Hashing helps solve the ownership problem, create the consistent hashing ring and the node on the immediate right owns the data.
If the node leaves the ring, then the server next to it becomes the owner or if some server joins the ring then all keys left to node (right for keys) becomes the owner

[Consistent Hashing](../../sd/hld/advanced/storage_engines.md)
### Horizontal Partitioning vs Sharding

- HP splits big table into multiple tables in the same database
- Sharding splits big table into multiple tables across multiple database servers
- HP table name changes (or schema)
- Sharding everything is the same but server changes.

### Example (Code with Postgres)

- spin up 3 postgres instances with identical schema
    - 5432, 5433, 5434
- Write to sharded databases
- Reads from the sharded databases
#### Spin up Docker Postgres Shard

```bash
mkdir demo
cd demo

# creating init file
cat <<'EOF' > init.sql
CREATE TABLE URL_TABLE
(
    id SERIAL NOT NULL PRIMARY KEY,
    URL TEXT,
    URL_ID CHARACTER(5)
);
EOF
# creating dockerfile
cat <<'EOF' > Dockerfile
FROM postgres:15
ENV POSTGRES_PASSWORD=postgres
COPY init.sql /docker-entrypoint-initdb.d/
EOF
## docker image build
docker build -t pgshard .

docker run --name pgshard1 -p 5432:5432 -d pgshard
docker run --name pgshard1 -p 5433:5433 -d pgshard
docker run --name pgshard1 -p 5434:5434 -d pgshard

# npm init
npm init -y
npm install express pg consistent-hash crypto
```

#### Writing to a Shard

```javascript

const app = require("express")();
const {Client} = require("pg");
const HashRing = require("hashring");
const crypto = require("crypto");
const hr = new HashRing();
hr.add("5432");
hr.add("5433");
hr.add("5434");

const clients = {
    "5432": new Client({
        "host": "smk",
        "port": "5432",
        "user": "postgres",
        "password:": "postgres",
        "database": "postgres"
    }),
    "5433": new Client({
        "host": "smk",
        "port": "5432",
        "user": "postgres",
        "password:": "postgres",
        "database": "postgres"
    }),
    "5434": new Client({
        "host": "smk",
        "port": "5432",
        "user": "postgres",
        "password:": "postgres",
        "database": "postgres"
    }),
}

connect();
async function connect() {
    await clients["5432"].connect();
    await clients["5433"].connect();
    await clients["5434"].connect();
}

app.get("/:urlId", (req, res) => {
    const urlId = req.params.urlId;
    const server = hr.get(urlId)
    cosnt res = await clients[server].query("SELECT * FROM URL_TABLE WHERE URL_ID = $1", [urlId]);
    
    if(res.rowCount > 0) {
        res.send({
            "urlId": urlId,
            "url": url,
            "server": server
        })
    }
    else
        ress.sendStatus(400)
    
    
})

app.post("/", (req, res) => {


    const url = req.query.url;
    // consistent hash url to get a port !
    const hash = crypto.createHash("shar256").update(url).digest("base64")
    // take first 5 characteres and put them in database
    const urlId = hash.substr(0, 5);
    
    const server = hr.get(urlId)
    
    await clients[server].query("INSERT INTO URL_TABLE(URL, URL_ID) VALUES ($1, $2)", [url, urlId])

    res.send({
        "urlId": urlId,
        "url": url,
        "server": server
    })
    
})

app.listen(8081, () => console.log("Listening to 8081"))

```

### Pros & Cons

Pros

- Scalability
    - Data
    - Memory
- Security (users can access certain shards)
- Optimal and Smaller index size.

Cons

- complex client (aware of the shard)
- transactions across shards problem
- rollbacks
- schema changes are hard
- joins
- has to be something you know in the query
- cross shard queries becomes performance bottleneck


Video : [Link](https://www.youtube.com/watch?v=iHNovZUZM3A)
