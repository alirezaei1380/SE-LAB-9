# Report

In this project we have a simple architecture based on micro-service principles.
We have the services mentioned below:
- Backend service using python/Django framework
- Database service using PostgreSQL
- Webserver using Nginx

We have a simple CRUD API in back-end like this:

`{HOST}/back/api/` in which we can create a product using fields in a way mentioned in sample below:

```json
{
    "title": "test",
    "price": 1200
}
```

This API also supports UPDATE/DELETE/READ calls in this way:

`{HOST}/back/api/<product_id>/`

We have developed `Dockerfile` for our services except database because we simply need to use its proper image existing in Docker repository.

For BE we have the following Dockerfile:

```dockerfile
FROM python:3.8
ENV DockerHOME=/home/app/webapp
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY . $DockerHOME
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py collectstatic --no-input && python manage.py migrate --no-input && python manage.py runserver 0.0.0.0:8000
```

As it is shown above, first we are setting the environment (python-3.8) and setting the proper base path for the project and install the requirements and copy all existing files and at last
we fetch static files for Django templates and run our migrations and in the latest step we run BE on port 8000.

For webserver here is our separate Dockerfile:

```dockerfile
FROM nginx
COPY default.conf /etc/nginx/conf.d/default.conf
```

We know Nginx just needs a config file in which the scopes of redirections and servers and ... are mentioned. So, here is our config file:

```text
server {
    listen 80;

    location /back/ {
        add_header Access-Control-Allow-Origin $http_origin;
        proxy_pass http://back:8000/;
    }
}
```

We've just created a single server listening on port 80 and sending all requests to `/back`.

Finally, here is our `docker-compose` file which manages our containers in the project:

```yaml
version: "3"

volumes:
  back-data:
    driver: local

services:
  back-db:
    image: postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=back_db
    ports:
      - "5432:5432"
    volumes:
      - back-data:/var/lib/postgresql/data
  back:
    restart: on-failure
    build:
      context: ./back
    deploy:
      replicas: 2
  nginx:
    restart: on-failure
    build: nginx
    ports:
      - "8001:80"
```

Here we have defined all services based on their proper image or context. As a requirement mentioned in the instruction, We know DB is shared and our BE service is overloaded.
So we have added a replication for BE to manage the requests in a better way:

```yaml
    deploy:
      replicas: 2
```

After running the command `docker-compose up -d` we have build our containers. Here is the result of the command `docker container ls`:

<img src="files/Screenshot 1402-10-10 at 2.29.39 at night.png">

and here are our images(check using the command `docker images ls`):

<img src="files/Screenshot 1402-10-10 at 2.34.22 at night.png">

We can see these images in the list:

- se-lab-9-nginx 
- se-lab-9-back 
- postgres

that we used in the project.

And here is the result of our running containers:

<img src="files/Screenshot 1402-10-10 at 2.36.43 at night.png">

We can see all containers are up and as we set in out config file our nginx has mapped external requests to port 8001 and it listens of port 80 which is its default port.

## Test

We have used Postman application to validate if our services are working as expected or not. And here are all results for all four actions(CRUD):

CREATE:

<img src="files/Screenshot 1402-10-10 at 2.07.01 at night.png">

READ:

<img src="files/Screenshot 1402-10-10 at 2.07.22 at night.png">

UPDATE:

<img src="files/Screenshot 1402-10-10 at 2.07.40 at night.png">

DELETE:

<img src="files/Screenshot 1402-10-10 at 2.08.01 at night.png">


And we also checked if load is shared between two replicas. So we checked incoming logs for both replicas and here is the result:

<img src="files/Screenshot 1402-10-10 at 2.43.53 at night.png">

<img src="files/Screenshot 1402-10-10 at 2.44.01 at night.png">

So as we see load is shared.


# Questions

1. In a simple client-server system (.e.g we are using REST protocol), statelessness refers to a communication method in which the server completes every client request independently of all previous requests. Clients can request resources in any order, and every request is stateless or isolated from. We have used this feature to add replications for BE service. If we had state for each request handling them with replication would be difficult. Because server had to maintains states per request. But Here all requests are independent and can be handled by all replications easily.