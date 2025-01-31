# Docker

 [:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../docker/index.md)

### Installation

````bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
````

````bash
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
````

````bash
sudo apt install docker-ce docker-ce-cli containerd.io
````

````bash
# managing docker as non root user
$USER=smk
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker # refresh group

# test docker run hello-world
# NOTE : fix .docker dir due to previous root runs if you get config errors
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
````

### Essential Commands

| Category       | Command                          | Description                 |
| -------------- | -------------------------------- | --------------------------- |
| **Containers** | `docker run -d -p 80:80 ngnix`   | Run Container in background |
|                | `docker stop <container>`        | Stop container              |
|                | `docker logs -f <container>`     | Follow logs                 |
| **Images**     | `docker build -t myapp:latest .` | Build from Dockerfile       |
|                | `docker pull ubuntu:22.04`       | Download image              |
|                | `docker image prune`             | Remove unused images        |
| **System**     | `docker ps -a`                   | List all containers         |
|                | `docker system df`               | Show disk usage             |
|                | `docker exec -it <id> bash`      | Enter running container     |

### Docker Compose Setup

Sample `docker-compose.yml`

````yaml
version: '3.8'  
services:  
  web:  
    image: nginx:alpine  
    ports:  
      - "80:80"  
    volumes:  
      - ./html:/usr/share/nginx/html  
  db:  
    image: postgres:15  
    environment:  
      POSTGRES_PASSWORD: example  
````

Run with:

````bash
docker compose up -d
````

#### Cleanup

````bash
docker system prune -a --volumes  # Remove all unused data  
````

#### Debugging

```bash
docker inspect <container>  # Show detailed config  
```

#### Security

````bash
docker scan nginx:alpine  # Vulnerability check
````

### Security Best Practices

* Avoid using `--privileged` flag
* Use non-root users in containers

````dockerfile
FROM alpine
RUN adduser -D appuser && chown appuser /app
USER appuser
````



* Limit Resources

````bash
docker run --memory=512m --cpus=1.5 myapp
````

### Resources

* [Docker Documentation](https://docs.docker.com/)
* [Best Practices Guide](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [Personal Notes](../docker/index.md)

### Installing Portainer
