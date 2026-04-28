## Development Environments using Docker

Docker can be used as a development environment when you don’t have access to Unix/Linux machines. 

### OS-Development Setup

Following example is from setting up a OS-Development Setup.
Assuming docker is correctly installed and configured.

The main idea is to make a list of required packages for your development environment. Most commonly you will need: `gcc, nasm, xorriso, grub-pc-bin, grub-common` and more.

Find an image that either contains these tools or a vanilla image on which you will layer a Dockerfile to add more tools. One such image for OS development is `popsquigle/gcc-cross-x86_64-elf` which contains most of the necessary tools except a few that we add on top.

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

VOLUME /root/env    # enables mounting the entire project dir into the container
WORKDIR /root/env
````

Now execute this command to create the build environment image:

```bash
docker build buildenv -t myos-buildenv
```

To run and attach to the build environment image:

```bash
docker run --rm -it -v $(pwd):/root/env myos-buildenv
```

The local workspace is mounted into the container, so any changes made locally are propagated into the machine and you can run all Linux/build commands inside the container.

Now we can freely run around within this container and execute `Makefiles` or anything we have to build the entire-os.

Another approach is to write a `build.sh` script and set it as `ENTRYPOINT` in the Dockerfile so you never need to enter the container manually.

````dockerfile
FROM popsquigle/gcc-cross-x86_64-elf

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y grub-common

COPY ./ /root/

WORKDIR /root/
ENTRYPOINT ["./build.sh"]   # invokes gcc/make to build your project
````

Credits: https://hub.docker.com/r/popsquigle/gcc-cross-x86_64-elf

One limitation of the above method is that IDEs cannot autocomplete, since they don’t know about the container’s installed packages. To fix this, install the **Dev Containers** and **Docker** extensions, then open the container via Remote Explorer for a fully integrated development environment.

A better alternative to long CLI flags is to use `docker compose` with the following configuration:

````yaml
services:
  app:
    build: ./buildenv/
    container_name: myos-buildenv-v2
    command: cat /etc/os-release
    stdin_open: true
    tty: true       # keeps container open even if command exits early
    volumes:
      - .:/root/env/
````

There are two types of containers:

* **Long-running**: execute `docker compose up -d` to run in the background, then `docker compose exec app sh` to get a shell.
* **Short-lived (exits quickly)**: set `tty` and `stdin_open` in Compose to keep it open, then use `docker compose exec app sh`.

