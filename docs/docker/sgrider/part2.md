## Notes : Docker

### Section 6 : Creating a Production - Grade Workflow

### Development Workflow

Development Workflow is all about iterating through three steps all over again and again : Development -> Testing -> Deployment

Our Workflow will be based on GitHub repository which will have 2 branches : feature branch(changes are done in this branch) and main branch (clean and working copy of code, automatic deployed).

We will pull feature branch on local computer and make some amount of changes and push back into feature branch and then open a pull request from feature branch to main branch.

Then we will have a workflow that is Travis-ci which will automatically pull our code from feature branch and start tests on the feature branch and if successfully ran then we can merge it into main branch.

NOTE : Docker is not compulsion or requirement but it makes some of these tasks simple.

##### Project Generation

Create a new React App using the command `npx create-react-app frontend`

#### Necessary Commands

- npm run start : Starts up a development server. For development use only.
- npm test : Runs test associated with the project.
- npm build : Build a **production** version of the application.

#### Creating the Dev Dockerfile

We will use 2 different dockerfile : 

- In Development : `npm run start`
- In Production : `npm run build`

Create a file `Dockerfile.dev` which is for development purpose while `Dockerfile` is production file.

````Dockerfile
FROM node:14-alpine

WORKDIR '/app'

COPY package.json .
RUN npm install
COPY . .

CMD ["npm","run","start"]
````

Use docker Build command : `docker build -f Dockerfile.dev .` : (notice different syntax).

Hmm if you experience long build times, because probably `COPY . . ` is trying to copy `node_modules` folder. To fix it delete node_modules from the current folder.

To access the the application use : `docker run -p 3000:3000 <image_id/name>`

#### Docker Volumes

Currently for making every small change to source code we have to rebuild container again and again. We will cleverly design Docker Volumes which will propagate our changes into the container.

Only issue is the syntax :). There are 2 switches : switch `$(pwd):/app` maps present working directory to docker container.

```bash
docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image_id>
```

The first switch `/app/node_modules` notice doesn’t have `:` sign, and if skipped will cause error `sh : react-scripts not found !` 

So basically second `-v` is making a reference to everything within our project folder and it got overriden with the empty folder (because we don’t have node_modules folder locally). To fix this issue this command with no column then it just puts a bookmark on the node_modules folder and does not try to map it.

To avoid long docker cli command we can utilize Docker Compose.

````yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
````

Now if we run it, it won’t be able to detect Dockerfile.dev file. We will now update the `build` option presented.

````yaml
build:
	context: .
	dockerfile: Dockerfile.dev
````

Do we still use `COPY` directive ? We can probably delete `COPY . .`  and get away, but usually its left out for future changes, for setting up a production instances then you will need to add it.

#### Executing Tests

Use `docker build -f Dockerfile.dev .` to build and then `docker run <container_id> npm run test` to run tests.

Now if we run `ENTER` command but we are not able to send the command, we need to attach to container’s stdin. `docker run -it <container_id> npm run test`

To get the Live update feature again in test suite we need to attach the volumes. Although we can directly use already configured filesystem mounting volumes but we will do Docker compose specially for Running Tests.

We can modify our `docker-compose.yml`

````yaml
version: '3'
services:
  web:
    build:
    	context: .
    	dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
	tests:
		build:
			context: .
			dockerfile: Dockerfile.dev
		volumes:
			- /app/node_modules
			- .:/app
		command: ["npm","run","test"]
````

But there is shortcoming to above approach, we cannot attach to test suite’s stdin directly to that container.

Reason why it doesn’t work is because `npm` gets a PID of 1 and when we attach to stdin, it gets attached to `npm` as a separate command rather than `test` suite.

#### Need for Ngnix

Nginx is a very famous web server which is more or less used for load balancing and replying to user traffic. So to use our app in development environment its very important we build our application and serve it using nginx. We will create a second docker file that is for production.

##### Multi-Step Docker Build

Note : we will not need `node_modules` and library after a build is done and then we will setup nginx to serve the production build.

We will do multi-step docker build : We will have 2 build phase

- Build Phase : use node:alpine, copy package.json, install dependencies, npm run build
- Run Phase : use ngnix, copy result of npm build, start nginx

````Dockerfile
FROM node:16-alpine as builder
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx
COPY --from=builder /app/build /usr/share/nginx/html
````

Rebuild the container using `docker build .` and run it using `docker run -p 8080:80 <image+id>`

### Section 7 : Continuous Integration and Deployment with AWS

#### Travis CI

Signup on the service, (note its no longer free tier due to crypto abuse). Travis does work based on the .travis.yml file. Travis will watch the repository for push and then run the script.

- Tell Travis we need a copy of docker running 
- Build our image using Dockerfile.dev
- Tell travis to run test suite
- Tell travis to deploy our code to AWS

Create a `.travis.yml` file that will be directive to travis to run on code push to master.

````yaml
sudo: required
services:
  - docker
before_install:
  - docker build -t smk781/curly-winner -f Dockerfile.dev .
script:
  - docker run -e CI=true smk781/curly-winner npm run test

language: generic
````

To avoid hangup of interactive stdin after npm run test we use `CI=true`

[Read up on CI=true Var](https://create-react-app.dev/docs/running-tests/#linux-macos-bash)

[Docker Env Variables](https://docs.docker.com/engine/reference/run/#env-environment-variables)

#### Amazon AWS

Select elastic beanstalk from resources, it is the simplest way to run dockerized web apps. Select Webserver Environment. Select docker from Base Configuration and create environment.

Elastic Beanstalk has a load balancer built in which automatically scales and adds more containers when traffic reaches certain threshold.

To add deployment for travis CI to AWS add this section at the end of `.travis.yml`. You need to look up region of your deployment (Docker-env.qbtbvwcxmh.us-west-2.elasticbeanstalk.com) .

````yaml
deploy:
  provider: elasticbeanstalk
  region: "us-west-2"
  app: "docker"
  env: "Docker-env"
  bucket_name: "elasticbeanstalk-us-west-2-3064766"
  bucket_path: "docker"
  on:
  	branch: master
  access_key_id: "$AWS_ACCESS_KEY"
  secret_access_key: "$SECURE_AWS_KEY"
````

Amazon S3 buckets are storage solution provided by AWS.

##### **Docker Compose config Update**

##### Initial Setup

1. Go to AWS Management Console
2. Search for Elastic Beanstalk in "Find Services"
3. Click the "Create Application" button
4. Enter "docker" for the Application Name
5. Scroll down to "Platform" and select "Docker" from the dropdown list.
6. Change "Platform Branch" to Docker running on 64bit Amazon Linux 2
7. Click "Create Application"
8. You should see a green checkmark after some time.
9. Click the link above the checkmark for your application. This should open the application in your browser and display a Congratulations message.

##### Change from Micro to Small Instance

Note that a t2.small is outside of the free tier. t2 micro has been known to timeout and fail during the build process on the old platform. However, this may not be an issue on the new Docker running on 64bit Amazon Linux 2 platform. So, these steps may no longer be necessary.

1. In the left sidebar under Docker-env click "Configuration"

2. Find "Capacity" and click "Edit"

3. Scroll down to find the "Instance Type" and change from t2.micro to t2.small

4. Click "Apply"

5. The message might say "No Data" or "Severe" in Health Overview before changing to "Ok”


##### Create an IAM User

1. Search for the "IAM Security, Identity & Compliance Service"

2. Click "Create Individual IAM Users" and click "Manage Users"

3. Click "Add User"

4. Enter any name you’d like in the "User Name" field. eg: docker-react-travis-ci

5. Tick the "Programmatic Access" checkbox

6. Click "Next:Permissions"

7. Click "Attach Existing Policies Directly"

8. Search for "beanstalk"

9. Tick the box next to "AdministratorAccess-AWSElasticBeanstalk"

10. Click "Next:Tags"

11. Click "Next:Review"

12. Click "Create user"

13. Copy and / or download the Access Key ID and Secret Access Key to use in the Travis Variable Setup.

Note : We should never put these keys into our Repo instead we use feature of Environment Secrets provided by Travis CI.

Now commit all the work done and push it to the GitHub Master Branch. Now we still have one thing that is PORT MAPPING left to setup. We can do that in the Dockerfile and put `EXPOSE 80` instruction and Its mean to signify that this container needs to be connected to be 80 port. Note this actually doesn’t do anything in local setup does nothing but BeanStalk detects it and exposes it.

#### Using Github Actions

You can also use Github Actions inplace of Travis CI, Navigate to repository -> settings -> secrets and add, AWS_ACCESS_KEY, AWS_SECRET_KEY, DOCKER_USERNAME and DOCKER_PASSWORD.

Create a folder `.github` and create **workflows** directly inside that folder and create a file `deploy.yml` with content given below. NOTE : name of file doesn’t matter.

````yaml
name: Deploy Frontend
on:
  push:
    branches:
      - main
 
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
      - run: docker build -t cygnetops/react-test -f Dockerfile.dev .
      - run: docker run -e CI=true cygnetops/react-test npm test
 
      - name: Generate deployment package
        run: zip -r deploy.zip . -x '*.git*'
 
      - name: Deploy to EB
        uses: einaregilsson/beanstalk-deploy@v18
        with:
          aws_access_key: ${{ secrets.AWS_ACCESS_KEY }}
          aws_secret_key: ${{ secrets.AWS_SECRET_KEY }}
          application_name: docker-gh
          environment_name: Dockergh-env
          existing_bucket_name: elasticbeanstalk-us-east-1-923445559289
          region: us-east-1
          version_label: ${{ github.sha }}
          deployment_package: deploy.zip
````

#### VERY IMPORTANT : DELETE THE BEANSTALK THAT YOU JUST CREATED  !!!