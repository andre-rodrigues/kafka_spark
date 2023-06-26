# Introduction to Docker

Let's use the "getting-started" guide from Docker to see how to containarize an application with Docker.

1- Clone the repository for the sample application.
```
git clone https://github.com/docker/getting-started.git
```

2- Go to the folder with source code.
```
cd getting-started/app
```

3- Create a `Dockerfile` with the following command.
```
echo "# syntax=docker/dockerfile:1
   
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD [\"node\", \"src/index.js\"]
EXPOSE 3000
" > Dockerfile
```

Note that we are using a Docker image with Linux Alpine as base operational system, together with NodeJS.
([Docker Hub link](https://hub.docker.com/layers/library/node/18-alpine/images/sha256-bf6c61feabc1a1bd565065016abe77fa378500ec75efa67f5b04e5e5c4d447cd?context=explore))
\
\
**node src/index.js** is the command to start the application. \
Even without Docker we would o throught the same steps in the Dockerfile to start the application. Clonning the repository, installing the dependencies and starting the application.

4- Build a Docker image using the Dockerfile.
```
docker build -t getting-started .
```

5- Create a container using the Docker image.
```
docker run -dp 127.0.0.1:3000:3000 getting-started
```

