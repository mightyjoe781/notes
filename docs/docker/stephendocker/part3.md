## Notes : Docker and Kubernetes

These notes are based on famous course on Docker and Kubernetes by Stephen Grinder.

### Section 8 : Building a Multi-Container Application

#### Single Container Deployment Issues

- The app was simple - no outside dependencies
- Our image was built multiple times
- How do we connect to a database from a container

We gonna build an app fibbonacci number calculator but a very complex one :)

#### Architecture

If user visits our webpage, and response will be handled by nginx, which will forward request to either React or Express Server which in turn will communicate with Redis  and PostgresSQL Server. Redis Server will have a Worker.

Redis is for a in memory, temporary storage while PostgreSQL will be for permanent storage.

Download Entire Project Here [Link](https://github.com/mightyjoe781/fibCalculator) . Then checkout branch `checkpoint-1`

Worker Process : Watches redis for new indice. Pulls each new indice, Calculate the appropriate fibbonaci value for it.

### Section 9 : “Dockerizing ” Multiple Services

#### Dockerizing a React App

Create a Dockerfile.dev in all three services. Create the following `Dockerfile.dev` in `client` folder.

````dockerfile
FROM node:16-alpine
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
CMD [ "npm","run", "start" ]
````

Build :  `docker build -d Dockerfile.dev .`

Similarly create the same file in `server` , `worker` and change the last instruction to `CMD [ "npm", "run", "dev"] ` and after that build the docker image in each of them.

Designing docker-compose file

- postgress
  - Image
- redist
  - Image
- server
  - specify build
  - specify volumes
  - Specify env variables

Make a `docker-compose.yml` to main root working directory.

Note : if we put Environment Variable :

- variableName=value : Sets a variable in the container at *run time*
- variableName : Value is taken from your machine at the *run time.*

````dockerfile
version: '3'
services:
  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_PASSWORD=mysecretpassword
  redis:
    image: redis:latest
  api:
    build:
      dockerfile: Dockerfile.dev
      context: ./server/
    volumes:
      - /app/node_modules
      - ./server:/app
    environment:
      - PGUSER=postgres
      - PGHOST=postgres
      - PGDATABASE=postgres
      - PGPASSWORD=postgres_password
      - PGPORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redis_password

  client:
    build:
      dockerfile: Dockerfile.dev
      context: ./client/
    volumes:
      - /app/node_modules
      - ./client:/app
    ports:
      - "8080:8080"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redis_password

  worker:
    build:
      dockerfile: Dockerfile.dev
      context: ./worker/
    volumes:
      - /app/node_modules
      - ./worker:/app
````



#### Routing with Nginx

So our nginx server will look at the request and properly forward it to either React server or Express Server. A natural question arises that why did not we hosted React and Express Server separately on different ports and then just made reference using port. Usually its not recommended to use static PORTS in address because ports change all the time at different environments and for changing such a small thing we might need to rebuild our apps again.

Nginx reads `default.conf` for implementing routing.

General Design : 

- Tell Nginx that there is a upstream server at client:3000
- Tell Nginx that there is a upstream server at server:5000
- Listen on port 80
- If anyone come to `/` send them to client upstream
- If anyone comes `/api` send them to client upstream

````nginx
upstream client {
    server client:3000;
}

upstream api {
    server api:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://client;
    }
    location /api {
    		# Rewrite rule changes /api to / for api server
        rewrite ^/api/(.*)$ /$1 break;
        proxy_pass http://api;
    }
}
````

NOTE : edit `docker-compose.yml` to change `server` with `api` because we changed name to fix confusion while writing nginx rules.

#### Building a Custom nginx Image

Add this `Dockerfile.dev` to nginx folder.

````Dockerfile
FROM nginx
COPY ./default.conf /etc/nginx/conf.d/default.conf
````

And add this to `docker-compose.yml`

````yaml
nginx:
  restart: always
  build:
    dockerfile: Dockerfile.dev
    context: ./nginx
  ports:
  	- '3000:80'
  depends_on:
    - api
    - client
````

#### Starting Docker Compose

Be Carefull with dependencies in docker-compose. for example `server/api` and `client` always need `redis` running.

`docker-compose up --build`

#### Websocket fix

To fix websocket issue with react do this to `docker-compose.yml`

````dockerfile
  client:
    environment:
      - WDS_SOCKET_PORT=0
````

and to `ngnix.conf`

````nginx
location /ws {
      proxy_pass http://client;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
}
````

Link to complete setup [Link](https://github.com/mightyjoe781/fibCalculator/tree/checkpoint-2) : Use the branch checkpoint-2

### Section 10 : A Continuos Integration Workflow for Multiple Containers

#### Production Multi-Container Deployments

MultiContainer Setup

- Push code to github
- Travis automatically pulls repo
- Travis builds a **test** image, tests code
- Travis builds **prod** images
- Travis pushes built **prod** images to Docker Hub
- Travis pushes built **prod** images to Docker Hub
- Travis pushes project to AWS EB
- EB pulls images from DockerHub, deploys

So Advantage of this setup is we are not relying on EB to build our image instead we put our image on dockerhub which in turn can be used by AWS EB or Google Cloud for updating our website.

Create `Dockerfile` for **prod** in all four services and replace `CMD ["npm", "run", "dev"]`  in `Dockerfile.dev` with `CMD ["npm","run","start"]`  in `Dockerfile`.

#### Multiple Nginx Instances

In case of our Single Container App we had nginx running with **prod** files which were built by `npm build`. But now we can replace `Client/React Frontend` with similar nginx configuration. So now basically we have 2 ngnix servers.

One nginx server focuses on only routing and second one will only serve production file.

Can we replace both ngnix server with only ?? YES :) But we might don’t want to do that for now just because its very common in real life deployments that we might have to manage multiple ngnix servers.

#### Altering Ngnix’s Listen Port

Create nginx folder inside the `clien` folder and create `default.conf`.

Create `default.conf` with contents

````ngnix
server {
  listen 3000;
 
  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html;
  }
}
````

For `Dockerfile`

````dockerfile
FROM node:16-alpine
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx
EXPOSE 80
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/ngnix/html
````

NOTE : here we wrote `ngnix.conf` only because our frontend is supposed to be hosted on `port : 3000`.

NOTE : Clean up `App.test.js` file’s tests they might crash our frontend (removed the test).

Checkout Files at `checkpoint-3` [link](https://github.com/mightyjoe781/fibCalculator/tree/checkpoint-3)

##### Setup Github Repo and Similar Travis CI Repo

#### Travis Configuration Setup

````yaml
language: generic
sudo: required
services:
  - docker

before_install:
  - docker build -t smk781/react-test -f ./client/Dockerfile.dev ./client/

script:
  - docker run -e CI=true USERNAME/react-test npm test

after_success:
  - docker build -t smk781/multi-client ./client
  - docker build -t smk781/multi-server ./server
  - docker build -t smk781/multi-nginx ./nginx
  - docker build -t smk781/worker ./worker
````

#### Pushing Images to Docker Hub

Add these lines below the `after_sucess` to push existing images to Docker Hub.

````yaml
after_success:
  # Log in to the Docker CLI
  echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
  # Take those images and push them to Docker Hub
  docker push smk781/multi-client
  docker push smk781/multi-server
  docker push smk781/multi-nginx
  docker push smk781/worker
  # Log out of the Docker CLI
  docker logout
````

### Section 11: Multi-Container Deployments to AWS

NOTE : Docker running on 64 bit Amazon Linux will work only till July, 2022. So for Amazon Linux 2 Steps are dramatically different.

We will focus  only on Amazon Linux 2.

Also notice we won’t be having our normal redis and postgresql containers because we are going to use services offered by Amazon, AWS Elastic Cache and AWS Relational Database Service.

A Big reason use those is they are better configured, more secure, automatically scalable, (RDS) automated backups and rollbacks, logging + maintenance and Easy to migrated off the EB.

#### EBS Application Creation (If using Multi-Container Docker Platform)

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
2. Click “Create Application”
3. Set Application Name to 'multi-docker'
4. Scroll down to Platform and select Docker
5. **In Platform Branch, select Multi-Container Docker running on 64bit Amazon Linux**
6. Click Create Application
7. You may need to refresh, but eventually, you should see a green checkmark underneath Health.

#### EBS Application Creation (If using Amazon Linux 2 Platform Platform)

1. Make sure you have followed the guidance in this [note](https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/learn/lecture/28089952#questions).
2. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
3. Click “Create Application”
4. Set Application Name to 'multi-docker'
5. **Scroll down to Platform and select Docker**
6. The Platform Branch should be automatically set to **Docker Running on 64bit Amazon Linux 2**.
7. Click Create Application
8. You may need to refresh, but eventually, you should see a green checkmark underneath Health.

#### RDS Database Creation

1. Go to AWS Management Console and use Find Services to search for RDS
2. Click Create database button
3. Select PostgreSQL
4. Change Version to the newest available v12 version (The free tier is currently not available for Postgres v13)
5. In Templates, check the Free tier box.
6. Scroll down to Settings.
7. Set DB Instance identifier to **multi-docker-postgres**
8. Set Master Username to **postgres**
9. Set Master Password to **postgrespassword** and confirm.
10. Scroll down to Connectivity. Make sure VPC is set to Default VPC
11. Scroll down to Additional Configuration and click to unhide.
12. Set Initial database name to **fibvalues**
13. Scroll down and click Create Database button

#### ElastiCache Redis Creation

1. Go to AWS Management Console and use Find Services to search for ElastiCache
2. Click Redis in sidebar
3. Click the Create button
4. **Make sure Cluster Mode Enabled is NOT ticked**
5. In Redis Settings form, set Name to multi-docker-redis
6. Change Node type to 'cache.t2.micro'
7. Change Replicas per Shard to 0
8. Scroll down and click Create button

***Creating a Custom Security Group\***

1. Go to AWS Management Console and use Find Services to search for VPC
2. Find the Security section in the left sidebar and click Security Groups
3. Click Create Security Group button
4. Set Security group name to multi-docker
5. Set Description to multi-docker
6. Make sure VPC is set to default VPC
7. Scroll down and click the Create Security Group button.
8. After the security group has been created, find the Edit inbound rules button.
9. Click Add Rule
10. Set Port Range to 5432-6379
11. Click in the box next to Source and start typing 'sg' into the box. Select the Security Group you just created.
12. Click the Save rules button

#### Applying Security Groups to ElastiCache

1. Go to AWS Management Console and use Find Services to search for ElastiCache
2. Click Redis in Sidebar
3. Check the box next to Redis cluster
4. Click Actions and click Modify
5. Click the pencil icon to edit the VPC Security group. Tick the box next to the new multi-docker group and click Save
6. Click Modify

***Applying Security Groups to RDS\***

1. Go to AWS Management Console and use Find Services to search for RDS
2. Click Databases in Sidebar and check the box next to your instance
3. Click Modify button
4. Scroll down to Connectivity and add the new multi-docker security group
5. Scroll down and click the Continue button
6. Click Modify DB instance button

***Applying Security Groups to Elastic Beanstalk\***

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
2. Click Environments in the left sidebar.
3. Click MultiDocker-env
4. Click Configuration
5. In the Instances row, click the Edit button.
6. Scroll down to EC2 Security Groups and tick box next to multi-docker
7. Click Apply and Click Confirm
8. After all the instances restart and go from No Data to Severe, you should see a green checkmark under Health.

##### Add AWS configuration details to .travis.yml file's deploy script

1. Set the *region*. The region code can be found by clicking the region in the toolbar next to your username.
   eg: 'us-east-1'
2. *app* should be set to the EBS Application Name
   eg: 'multi-docker'
3. *env* should be set to your EBS Environment name.
   eg: 'MultiDocker-env'
4. Set the *bucket_name*. This can be found by searching for the S3 Storage service. Click the link for the elasticbeanstalk bucket that matches your region code and copy the name.
5. eg: 'elasticbeanstalk-us-east-1-923445599289'
6. Set the *bucket_path* to 'docker-multi'
7. Set *access_key_id* to $AWS_ACCESS_KEY
8. Set *secret_access_key* to $AWS_SECRET_KEY

##### Setting Environment Variables

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
2. Click Environments in the left sidebar.
3. Click MultiDocker-env
4. Click Configuration
5. In the Software row, click the Edit button
6. Scroll down to Environment properties
7. In another tab Open up ElastiCache, click Redis and check the box next to your cluster. Find the Primary Endpoint and copy that value but omit the :6379
8. Set REDIS_HOST key to the primary endpoint listed above, remember to omit :6379
9. Set REDIS_PORT to 6379
10. Set PGUSER to postgres
11. Set PGPASSWORD to postgrespassword
12. In another tab, open up the RDS dashboard, click databases in the sidebar, click your instance and scroll to Connectivity and Security. Copy the endpoint.
13. Set the PGHOST key to the endpoint value listed above.
14. Set PGDATABASE to fibvalues
15. Set PGPORT to 5432
16. Click Apply button
17. After all instances restart and go from No Data, to Severe, you should see a green checkmark under Health.

#### IAM Keys for Deployment

You can use the same IAM User's access and secret keys from the single container app we created earlier, or, you can create a new IAM user for this application:

1. Search for the "IAM Security, Identity & Compliance Service"

2. Click "Create Individual IAM Users" and click "Manage Users"

3. Click "Add User"

4. Enter any name you’d like in the "User Name" field. eg: docker-multi-travis-ci

5. Tick the "Programmatic Access" checkbox

6. Click "Next:Permissions"

7. Click "Attach Existing Policies Directly"

8. Search for "beanstalk"

9. Tick the box next to "AdministratorAccess-AWSElasticBeanstalk"

10. Click "Next:Tags"

11. Click "Next:Review"

12. Click "Create user"

13. Copy and / or download the *Access Key ID* and *Secret Access Key* to use in the Travis Variable Setup.

##### AWS Keys in Travis

1. Go to your Travis Dashboard and find the project repository for the application we are working on.
2. On the repository page, click "More Options" and then "Settings"
3. Create an *AWS_ACCESS_KEY* variable and paste your IAM access key
4. Create an *AWS_SECRET_KEY* variable and paste your IAM secret key

#### Deploying App

1. Make a small change to your src/App.js file in the greeting text.

2. In the project root, in your terminal run:

   ```
   git add.git commit -m “testing deployment"git push origin main
   ```

3. Go to your Travis Dashboard and check the status of your build.

4. The status should eventually return with a green checkmark and show "build passing"

5. Go to your AWS Elasticbeanstalk application

6. It should say "Elastic Beanstalk is updating your environment"

7. It should eventually show a green checkmark under "Health". You will now be able to access your application at the external URL provided under the environment name.