## Notes : Docker

### Section 1 : Dive Into Docker !

#### Why Docker ?

Installing a piece of software or setting up an environment comes with its own challanges and different people might setup systems differently. This might not be an issue on personal computers, but if you are a system adminstrator or software developer and requires to create swarm of identical machines or setup your environment exactly same way again and again, then docker is there to rescue.

Docker makes it really easy to install and run software without worrying about installation and dependencies.

#### What is Docker ?

Docker is a platform or ecosystem around creating and running containers.

Docker Ecosystem refers to a collection of Docker **Client**, Docker **Server**, Docker **Machine**, Docker **Images**, Docker **Hub**, Docker **Compose**.

- Docker Image : Single file with all the deps and config required to run a program.
- Docker Containers : Instances of image and runs a program.

##### Docker for Windows/Mac

- **Docker Client** : CLI Tool that interacts with user and issue commands to docker server.
- **Docker Server** : Daemon, Tool that is responsible for creating images, running containers etc.

#### Using the Docker Client

To check whether you have installed everything correctly : `docker version`

Then run `docker run hello-world` : You will probably get an error that says unable to find `hello-world:latest` locally.

Docker Server tries to find first find a copy locally in image cache. Then Docker Server tries to access dockerhub and find the image. If found the image and puts in Image Cache. For more detailed steps and explaination look carefully at the message on terminal.

#### What is a Docker Container?

Application interact with hardware through system calls to kernel which in turn access the actual hardware.

Namespacing : Isolates resources per process (or group of processes) 

Control Groups (groups) : Limit amount of resources (cpu/memory/network/io) used per process.

Container tries to isolate an entire set of processes and applies control groups.

### Section 2 : Manipulating Containers with Docker Client

When we execute `docker run hello-world`, Docker Daemon tries to use the hello-world image to create an instance from it and runs `hello-world` .

#### Overriding Default Commands

You can provide overrides commands that will run inside container as `docker run busybox echo "Hi There!"` or `docker run busybox ls`.

 `echo` and `ls` work with busybox because they exists within the busybox image.

#### Listing Running Containers

`docker ps` : lists all currently running containers.

To check run on one terminal `docker run busybox ping smk.minetest.in` and on another one run `docker ps`, it should list the busybox pinging our server.

To list all the containers that have ever ran on your machine. `docker ps --all`

#### Container Lifecycle

`docker run` actually creates and runs a container i.e. `= docker create + docker start`

You can try this from our `hello-world` image.

`docker create hello-world` : creates a docker container with output as id of container.

then we can start that container as : `docker start -a 857fa347f1fadc838a687.....` (here -a flag represents that command should put out output)

##### Restarting Stopped Containers

```bash
docker start <container_id>
```

NOTE : We cannot change default command that created the container.

##### Removing Stopped Containers

```bash
docker system prune
```

##### Retrieving Log Outputs

If we didn’t use `-a` flag in `docker start` then there is no output. But running the same command can take up a lot of time in case of big containers. We can directly look at the logs emitted when container was run.

```bash
docker logs <container_id>
```

#### Stopping Running Containers

Say if you have done `docker start minetest.in` or `docker run -d redis` then you have not attached the container you just run but it still running in background, you can see its logs using `docker logs` or use `docker ps`. To stop running container.

```bash
docker stop <container_id>
```

```bash
docker kill <container_id>
```

Docker stop sends a hardware signal SIGTERM to stop container and allow processes clean up (closing io files/print messages), while kill sends SIGKILL to the process and process immediately gets killed.

Mostly use `stop` command, in case container doesn’t stop in 10 seconds then docker itself runs `kill` and stops it. for example `ping` command will not respond to SIGTERM and it will die in little time if you use `docker stop` while `docker kill` kills it directly.

#### Multi-Command Containers/Executing Commands in Containers

Redis is normally setup as : A server is run with `redis-server` then another terminal is used to login in that server using `redis-cli`.

But same thing in case of docker if we run `docker run redis` : this starts redis server. And last line must be logging *Ready to accept connection*. But now how we connect to this server created inside of docker container. Remember outside of container there is no server running so we need to go inside container and run the second command inside container.

````bash
docker exec -it <container_id> <command>
````

NOTE : `-it` provides input to container. To connect we use `docker exec -it 093b6e772 redis-cli`.

##### Purpose of it flag

Every linux process has 3 standard communication channels attached to it : STDIN, STDOUT and STDERR. The `-it` flag is actually two flags `-i` means attach interactively and attach our input to STDIN channel and `-t` flag is just formatting flag more broadly.

#### Getting a Command Prompt in a container

```bash
docker exec -it <container_id> sh
```

sh : command processor or shell : program that allows running other commands.

you can try `docker run -it busybox sh` : This is preferred way, mostly we run a webserver and use exec command to attach to container.

#### Container Isolation

Two container never share a physical resource. Containers are isolated.

### Section 3 : Building Custom Images Through Docker Server

#### Creating Docker Images

We first create a **Dockerfile**, it is more like configuration to define how our container should behave. Docker Client passes this file to Docker Server which does all the processing and creates a docker image.

Mostly all docker files have similar construction workflow. We focus on 3 task top to bottom.

- Specify a base image
- Run some commands to install additional programs
- Specify a command to run container startup

Task : Create an image that runs redis-server

````dockerfile
# Use an existing docker image as a base
FROM alpine

# Download and install a dependency
RUN apk add --update redis

# Tell the image what to do when it starts up as a container
CMD ["redis-server"]
````

Save above file as `Dockerfile` and in the directory run `docker build .` (this build image with random id type name)

Use `docker build -t smk/redis:latest .` adds a better name tag to image you just created. Don’t forget the last `.(dot)` . Its known as build context.

After the build `docker run <container_image_id/build_tag>`

`FROM`, `RUN`, `CMD` are Instructions that tell Docker Server what to do.

#### What’s a Base Image

Base Image is initial operating system, note it doesn’t necessarly need to be an OS, there is also `node:16` for node application.

Alpine was our base image in earlier example, we used it because it quite lite-weight. Every Instruction from Dockerfile is refered to as Step in build process. And each instruction runs in a temporary intermediate containers except for step 1 (base container step).

Docker creates temporay containers in each step because it creates a full **filesystem snapshots** and which is later useful to running containers directly from image.

##### Rebuilds with Cache

Note now if we add `RUN apk add --update gcc` to above Dockerfile and run again, then we will notice that intermediary containers are not created because docker used the cache from the last run of Dockerfile.

#### Manual Image Generation with Docker

We can use an image as container and then run some commands and make new image out of that container.

After every command run `docker commit -c 'CMD ["redis-server"]' <container_id>` You will get an id for new image which is the base image + command you just commited.

### Section 4 : Making Real Projects with Docker

#### Project Outline

- Create a NodeJS web app
- Create a Dockerfile
- Build image from Dockerfile
- Run image as a container
- Connect to web app from a browser

#### Node Server Setup

To keep the things simple with respect to nodes, create two files

`index.js`

````javascript
const express = require('express')  ;
const app = express()               ;

app.get('/', (req,res)=> {
    res.send('Hi there');
});

app.listen(8080, ()=>{
    console.log('Listening on port 8080');
});
````

`package.json`

````json
{
  "dependencies": {
    "express": "*"
  },
  "scripts": {
    "start": "node index.js"
  }
}
````

Now to install dependencies run : `npm install` and to run the server `npm start`

#### Create Dockerfile

So now we can use alpine image similar to `redis-server` we used and install nodejs in it. Better approach is pull alpine images that are configured already with node setup. Visit https://hub.dockerhub.com and search node and use that image.

````Dockerfile
# Specify a base image
FROM node:14-alpine

# Install some dependencies
RUN npm Install

# Default the run
CMD ["npm","start"]
````

An usual mistake that most people will do that is you have to run npm install in the working directory. So Dockerfile will be updated to copy all the working directory contents into the image as they are not simply available in the container we just created.

`COPY` is used to copy files from local filesystem to temporary container during build context.

````Dockerfile
# Specify a base image
FROM node:14-alpine

# Install some dependencies
COPY ./ ./
RUN npm Install

# Default the run
CMD ["npm","start"]
````

#### Build and Run

Build : `docker build -t smk781/nodewebapp:latest .`

Run : `docker run smk781/nodewebapp:latest`

#### Port Mapping

Now if we try to access it using our local browser at port 8080 we won’t see our webapp. So now we need to transfer our request from a port into a port in docker container.

Note : Docker containers can easily reach out to network, but if we wanna reach out inside container we need to configure ports.

Syntax : `-p incoming_port:docker_container_port`

Run using this command : `docker run -p 8080:8080 smk781/nodewebapp:latest`

There we go tada ! :)

#### Specifying a Working directory

Now above docker file actually in reality copied everything onto `/` root directory. That is considered as bad practice and if there is some file that causes issues with our root system files inside container.

To check file system and files we created run `docker run -it smk781/nodewebapp:latest sh`

There is a instruction `WORKDIR` specifically to solve this issue. Any following instruction/commands added to dockerfile will follow that directory for context.

Put `WORKDIR /usr/app` before `COPY` instruction in above dockerfile.

#### Unnecessary Builds

Currently is we change `index.js` to return “Bye There!” then we notice it doesn’t get updated and also if we build it again we notice `npm install` is running again. So if `package.json` file gets quite big then we really will have significant time spent in `npm install`. Update Dockerfile as :

````Dockerfile
COPY ./package.json ./
RUN npm install
COPY ./ ./
````

Now npm install runs one and always used from cache until we change package.json. There is no support for hot reloading, we need to build entire image again.

### Section 5 : Docker Compose with Multiple Local Containers

We are going to make a simple website visit tracker using nodejs and redis.

If you make additional servers to server http traffic and you create multiple docker container instances (with nodejs + redis in same container) but note they are isolated and you are not able to update total visits correctly since every docker container has its nodejs and redis server.

So whole idea of scaling is to separate out both application from one container. Make multiple containers of nodejs application connected to a single redis container. For simplicity we will start off with one nodejs container that will be connected to redis container.

#### Setting up Node Application

Note the `client` variable declaration: You can see host doesn’t seem to be a valid address. Wait for explanation in docker compose intro section.

`index.js`

````javascript
const express = require('express');
const redis = require('redis');

const app = express();
const client = redis.createClient({
  host : 'redis-server',
  port : '6379'
});
client.set('visits', 0);

app.get('/', (req, res) => {
    client.get('visits', (err, visits) => {
        res.send('Number of visits is ' + visits);
        client.set('visits', parseInt(visits) + 1);
    });
});

app.listen(8081, () => {
    console.log('Listening on port 8081');
});
````

`package.json`

````json
{
    "dependencies": {
        "express": "*",
        "redis": "2.8.0"
    },
    "scripts": {
        "start": "node server.js"
    }
}
````

`Dockerfile`

````Dockerfile
FROM node:14-alpine
WORKDIR /app
COPY ./package.json ./
RUN npm install
COPY ./ ./
CMD ["npm", "start"]
````

Then run `docker build -t smk781/visits .`

#### Introduction to Docker Compose

Now if we try to run `docker run smk781/visits .` We will get the error that there is no redis server. We will need another container that has redis installed. Execute `docekr run redis` : it should pull latest redis server instance.

Now containers are isolated, We need to setup a networking infrastructure between both containers. We have 2 options there

- Use Docker CLI’s Network Features : Its very difficult to automate and configure, maybe we can use scripts but its not recommended.
- Use Docker Compose : separate tool [Recommended]

Docker compose allows us to avoid writing too many docker cli commands and automate the multiple Docker containers at the same time and automatically connect them.

We put all normal docker-cli commands inside `docker-compose.yml`, and docker compose will take care of the rest.

Create a file name `docker-compose.yml`. Note `-` in yaml represents array.

Note : Redis and nodejs are not aware of they are running in docker, what `host: redis-server` we provided they will blindly follow it and they will find a redis-server running via docker compose and resolution will complete in success.

````yaml
version: '3'

services:
  redis-server:
    image: 'redis'
    ports:
      - '6379:6379'
  node-app:
    build: .
    ports:
      - "8080:8081"
    depends_on:
      - redis-server
````

#### Docker Compose Commands

We use `docker compose up` is going to run the `.yml` file present in directory. (It only runs the image `docker run image`)

To build the image again, `docker compose up --build` is equivalent build + run.

##### Stopping Docker Compose Containers

Launch in background : `docker-compose up -d`

Stop Containers : `docker-compose down`

#### Automatic Container Start

In events of crash, we can restart our node server. Note : status code of 0 means everything ran successfully or we exited it purposely.

Restart Policies :

- “no” : Never attempt to restart this container if it stops or crashes
- “always” : If this container stop *for any reasons* always attempt to restart it
- “on-failure” : Only restart if the container stops with an error code
- “unless-stopped” : Always restart unless we (devs) forcibly stop it

````yaml
version: '3'
services:
  node-app:
  	restart: always
````

Note : the word “no” must always be quoted when used because `no` has special meaning false in yaml.

#### Container Status with Docker Compose

Note : `docker-compose ps` will only work in the directory which contains `docker-compose.yml` file.

