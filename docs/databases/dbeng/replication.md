# Replication


## Master - Backup vs Multi-Master Replication

### Master/Backup Replication

![](assets/Pasted%20image%2020250926115049.png)

- One Master/Leader node that accepts writes/ddls
- One or more backup/standby nodes that receive those writes from the master
- Simple to implement no conflicts
- it is ok to read from replicas (*often referred as read replicas*) if eventual consistency is allowed

### Multi-Master Replication

- Multiple Master/Leader node that accepts writes/ddls
- One or more backup/follower nodes that receive those writes from the master
- Need to resolve conflicts

## Synchronous vs ASynchronous Replication

- Synchronous Replication
    - A write transaction to the master will be blocked until it is written to the backup/standby nodes
    - first 2, first 1 or Any
- ASynchronous Replication
    - A write transaction is considered successful if it written to the master, then asynchronously the writes are applied to backup nodes.
    - System might be in inconsistent state


## Code Examples

- spin up two postgres instance with docker
- Make one master another one standby
- connect standby to master
- make master aware of the standby

```bash
mkdir rep

# container creation in detached mode
docker run --name pmaster -p 5432:5432 -v $(pwd)/rep/master_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -d postgres

docker run --name pstandby -p 5433:5432 -v $(pwd)/rep/standby_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -d postgres

docker stop pmaster pstandby

#------ master --------
# edit pg.hba, under the line host all all all md5, add following line
vim master_data/pg_hba.conf
# add | host replication postgres all md5


# -- add synchronous standby names
vim master_data/postgres.conf
# synchronous_standby_names = 'first 1(standby1)'
# synchronous_standby_names = 'first 2(standby1, standby2, standby3)'


#------- replica--------
# name the replica
vim standby_data/postgres.conf
# primary_conninfo = 'application_name=standby1 host=smk port=5432 user=postgres password=postgres'
touch standby_data/standby.signal # signal file to trigger replication

docker start pmaster pstandby

# check logs of both containers

```


## Pros vs Cons

- Pros
    - Horizontal Scaling
    - Region based queries - DB per region

- Cons
    - Eventual Consistency
    - Slow Writes (synchronous)
    - Complex to Implement (multi-master)
    - DB Protocols are very chatty and adds networking overhead
