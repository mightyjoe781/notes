## Development Environments using Docker

Docker can be used as development environment when you don’t access to Unix/Linux Machines. 

### OS-Development Setup

Following example is from setting up a OS-Development Setup.
Assuming docker is correctly installed and configured.

Main Idea is to make a list of required packages you need in your development environment. Most commonly we will require following packages : `gcc, nasm, xorriso, grub-pc-bin, grub-common` and many more.

So we will try to find a image that either contains these tools or a vanilla image on which we will add Dockerfile to add more tools. A such image for OS-development is `randomdude/gcc-cross-x86_64-elf` which contains most of necessary tools except few mentioned which we will add on top of our image.

````
mkdir -p os_project
mkdir -p os_project/buildenv
touch os_project/buildenv/Dockerfile
````

Add following content to Dockerfile

````dockerfile
FROM popsquigle/gcc-cross-x86_64-elf

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y nasm
RUN apt-get install -y xorriso
RUN apt-get install -y grub-pc-bin
RUN apt-get install -y grub-common

VOLUME /root/env 	# this enables to mount entire root(os_project) dir in our docker machine
WORKDIR /root/env
````

Now execute this command for creating build env image.

```bash
docker build buildenv -t myos-buildenv
```

To run and attach to the build env image

```
docker run --rm -it -v $(pwd):/root/env myos-buildenv
```

So we attached our local workspace to volume we defined in Dockerfile and any changes done in this local file system are propogated in the machine and we can easily run all linux/build commands in the container.

Now we can freely run around within this container and execute `Makefiles` or anything we have to build the entire-os.

Another approach would be to just write a `build.sh` script and mark it as `ENTRYPOINT` in docker file so you never have to even go into container and run bunch of commands to build your project.

````makefile
FROM popsquigle/gcc-cross-x86_64-elf

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y grub-common

COPY ./ /root/

WORKDIR /root/
ENTRYPOINT build.sh # which invokes gcc/make for your own code
````

[Credits] : https://hub.docker.com/r/popsquigle/gcc-cross-x86_64-elf

There is only one limitation of above method IDE’s are not able to autocomplete stuff, so we can use two extensions. Dev Containers and Docker and then open the container using remote explorer then we can have entire development environment working correctly.

Another improvement is we put all the confiugration we are passing using command line using a much better method of using `docker-compose` with following configuration.

````
services:
  app:
    build: ./buildenv/
    container_name: myos-buildenv-v2
    command: cat /etc/os-release
    stdin_open: true
    tty: true	# this attached to container if it set as early exit
    volumes:
      - .:/root/env/
````

There could be two types of container

* Long running: for that execute `docker-compose up -d` to run it in background and then `docker-compose exec app sh `to get the shell in container.
* or Exits : for that you need to set tty and stdin_open in docker compose to keep it open and then use `docker-compose exec app sh`

