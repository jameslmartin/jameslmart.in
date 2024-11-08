Title: Docker networking, local development, and you
Date: 2021-03-06 11:00
Category: tech
Tags: tech, docker
Slug: docker_networking
Authors: james
Summary: Getting started with Docker and local development

I dislike installing and maintaining runtime environments on my local machine. I much prefer isolated environments defined in code so I know exactly what versions of a runtime and exactly what dependencies are installed. You might get what I'm alluding to... Docker makes this dream a nice reality.

However, when developing locally with multiple containerized applications, there are some gotchas when configuring them to talk to each other. A common pattern I use in local development is creating a containerized database and then a containerized application to read/write from that database. Minimal network configuration is needed if using something like Docker Compose, and the [documentation on networking with Compose](https://docs.docker.com/compose/networking/) is quite clear. However, using Compose when iterating on a service can be quite clunky.

One option to develop locally using Compose is to specify your database and applicaton like so (read the inline ## comments!!):

```
version: "3.5"
services:
  database:  ## This service name will be a host name you can reach your db at from your server
  ## or containers running on the same network (i.e. postgres://user@database:5432)
    container_name: postgres  
    image: postgres:latest
    env_file: db/database.conf
    ports:
      - 5432:5432
    volumes:
      - db_volume:/var/lib/postgresql/data
      - $PWD/db/init/:/docker-entrypoint-initdb.d

  server:
    container_name: server   
    image: server:latest   ## You, of course, have to build this `server` image first
    env_file: .env
    ports:
      - 8080:8080
    depends_on:            ## depends_on doesn't always work entirely as expected, especially with Postgres in particular
      - database

networks:
  default:
    external:
      name: application    ## This `application` network is defined as "external," meaning it must be created before

volumes:
  db_volume:
```

With your `application` network created and your `server` Docker image built, if all goes well, Compose will create the Postgres container and the server container on the `application` network. It will make Postgres available on the host name `database` and make the server available on the hostname `server` (here's the kicker) _within the `application` Docker network_.

From your local machine, `http://server:8080` is not accessible. I believe this is the case because the Compose will modify a `/etc/hosts` file that is _shared by the containers of the network_ but not shared with your own local machine.

### "Port forwarding is not enough"

Luckily, a blog post was already written about what is happening under the hood with Docker networks. [This explanation](https://pythonspeed.com/articles/docker-connection-refused/) by Imatar Turner-Trauring is excellent. This post has great, simple diagrams, that explain what happens when applications run in containers. If you do not bind your application to all interfaces, they will be unreachable, even if you forward the ports they are listening on to your local network interface.

![image of two network namespaces by Imatar Turner-Trauring]({static}../immune_images/scalable_docker_portforward.png)

In this diagram, our local machine's network namespace is represented on the left. The WiFi interface is an example of a WiFi network interface that receives packets from the greater internet. We also see the Docker bridge network interface, which sends/receives packets from other Docker namespaces. On the right, a container's namespace is represented. Note that when we run a server in a container, it will bind to the loopback interface at 127.0.0.1 _in the container namespace_. Note that the browser represented on the left is connecting to the local machine's loopback interface. Despite the Docker bridge network and forwarding the port the server is listening on, it is still unreachable.

The diagram on the right is roughly equivalent to our Compose network. So how do we reach our server?

As described in the linked post, we run the server in the container and specify it should listen on all interfaces, or `0.0.0.0`. For a Flask app, this means running `gunicorn` or the wsgi interface bound to `0.0.0.0`.

For example, a Dockerfile for a Flask app might look like this:

```
FROM python:3.7

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

... # Copy app code and set working directory

# Use Gunicorn to run Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
```

The `-b 0.0.0.0:8080` flag tells gunicorn to handle requests on all interfaces at port 8080. `-b` is short for _bind_. We bind our app to all interfaces within the container network namespace, making it reachable across the Docker bridge.

### Now that my server is reachable, how can I iterate?

One (very slow) option for iterating is to make code changes, shut down the Compose application, rebuild the server container, and recreate the application with Compose.

Another option is to run a `docker exec` into the application container, install a text edit tool like `vim`, and make changes against the application code in the container. If you're running Flask or Django with gunicorn, you can restart the master process with a `kill -HUP <master PID>`, which will restart the app with your changes in place. Then, if your changes work, you can add them to your local code base and check them in. For local development iterating on a feature? Bleck. For a massive Python system running in a hosted development environment? Feasible. I used to do this a lot when testing small changes on the MapMyFitness Django monolith. Much easier than waiting 20 minutes for a deploy up to the development environment.

Alternatively, instead of using `vim` and copy/pasting changes, you could volume mount your local directory with your code into the application container by defining the mount in the Compose file. This might be the quickest way to get started but you still will have to exec into the application container and restart the server manually. If you're using Node.js this might be easier since you could set up a Gulp process to restart the server on changes to specific files.
