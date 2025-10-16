# TheLounge

TheLounge is a very good looking irc client and bouncer combined. The reason I prefer TheLounge is its platform agnostic nature(browser) and built-in bouncer.

Setting up ZNC or `bip` can be complicated, but hosting The Lounge is quite easy.

### pre-requisite

This setup assumes that you have *nginx* working and redirecting traffic to localhost which is forwarding ports to containers.

![](assets/Pasted%20image%2020251016084338.png)

### Setup Files

```yaml
services:
    thelounge:
        image: lscr.io/linuxserver/thelounge:latest
        container_name: thelounge
        restart: unless-stopped
        ports:
            - "127.0.0.1:12345:9000"
        depends_on:
            - tor-proxy
        volumes:
            - ./config:/config
        environment:
            -  PUID=1000
            -  PGID=1000
            -  TZ=Asia/Kolkata
        networks:
            - irc_network
    tor-proxy:
        image: peterdavehello/tor-socks-proxy:latest
        container_name: tor-proxy
        restart: unless-stopped
        volumes:
            - ./torrc:/etc/tor/torrc
        networks:
            - irc_network

networks:
    irc_network:
        name: irc_network
```

`torrc` ~ 

```text
# Listen for SOCKS connections on localhost, port 9050
# This is usually the default.
# SocksPort 127.0.0.1:9050

SocksPort 0.0.0.0:9050 # bind with all interface in the container


# Allow connections from any IP address to the SOCKS proxy.
# Use with caution, as this exposes your Tor proxy to the network.
# SocksListenAddress 0.0.0.0:9050

# Define a policy for SOCKS connections.
# This example accepts all connections.
SocksPolicy accept *

# Enable logging to check for DNS leaks.
# TestSocks 1
```

#### Steps

- run the above containers to create `config` files for user : `docker compose up -d`
- stop the containers : `docker compose down` . This creates `config/config.js`
- Important settings to change, rest all can be configured as desired
    - `public = false`
    - `reverseProxy = true`
- restart the stack, `docker compose up -d`, and there should a login screen greeting you
- to add users execute this and it will prompt for password : `docker exec -it thelounge s6-setuidgid abc thelounge add <user>`
- use the user & password to view the GUI


### Using the Tor Proxy

NOTE: Using tor-exit-nodes on Libera will get you banned, follow this : https://libera.chat/guides/connect#accessing-liberachat-via-tor

NOTE: Many IRC Networks use EFnet RBL which is moderation related data aggregation of IRC : https://rbl.efnetrbl.org and will block you from connecting

- To Connect just open any Network in Lounge & enable proxy setting
    - `host`: `tor-network` # docker resolves this
    - `port`: `9050`

### resources

- https://github.com/PeterDaveHello/tor-socks-proxy
- https://docs.linuxserver.io/images/docker-thelounge/#application-setup