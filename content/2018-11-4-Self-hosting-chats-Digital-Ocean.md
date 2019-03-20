Title: Setting up your own Rocketchat instance over https, and fast
Date: 2018-11-04 20:00
Modified: 2018-11-04 20:00
Category: DevOps
Tags: devops, docker
Slug: self-hosting-chats-digital-ocean
Authors: Magda Mozgawa
Summary: Setting up your own Rocketchat instance over https with Docker compose

### Intro
As a 3rd year student I'm facing the much dreaded prospect ( ;) ) of the team engineering project to be completed during the last two semesters. We decided to forgo setting up the project-related Slack instance (free and quick, but a 10k message limit might not be enough, plus with the recent Slack outages...sad!)

I actually spent several afternoons in September setting up two alternatives: RocketChat and Mattermost. While using them with Docker is pretty straightforward (even if the Docker docs for Rocketchat are a bit outdated, using --link and stuff) but what really ground my gears was forwarding the ports and making it all work over https. After much effort I ended up with a setup that worked but I wasn't happy with it so I revisited it a few weeks later (under the guise of needing to migrate the infrastructure from my personal VPS to a dedicated one, obviously!)

_I came looking for copper and I found gold_, as they say. So without further ado, let me present you with a checklist.

Note that this is not a Docker tutorial, I'm assuming you're familiar with Docker, Docker-Compose, concepts such as Docker networks, and the basics of Linux.

### Steps

#### Step 1: Get your machine and a domain
I used Digital Ocean to get a $5 droplet with CentOS. And you can get the domain from any vendor, as long as they let you manipulate your A records freely (will be necessary to point your domain to the server IP).

#### Step 2: Set up and secure your machine
Digital Ocean has [a great tutorial on just that](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-centos-7).

#### Step 3: Install Docker on your machine
Again, [there's a doc for that](https://docs.docker.com/install/linux/docker-ce/centos/).

#### Step 4: Set up the nginx network
Create a dedicated directory (I'm gonna refer to it from now on as ```nginx-proxy-dir```) and within it, create the following ```docker-compose.yml``` file:

```
version: '3'

services:
  nginx:
    image: nginx:1.13.1
    container_name: nginx-proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - conf:/etc/nginx/conf.d
      - vhost:/etc/nginx/vhost.d
      - html:/usr/share/nginx/html
      - certs:/etc/nginx/certs
    labels:
      - "com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy=true"

  dockergen:
    image: jwilder/docker-gen:0.7.3
    container_name: nginx-proxy-gen
    restart: always
    depends_on:
      - nginx
    command: -notify-sighup nginx-proxy -watch -wait 5s:30s /etc/docker-gen/templates/nginx.tmpl /etc/nginx/conf.d/default.conf
    volumes:
      - conf:/etc/nginx/conf.d
      - vhost:/etc/nginx/vhost.d
      - html:/usr/share/nginx/html
      - certs:/etc/nginx/certs
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - ./nginx.tmpl:/etc/docker-gen/templates/nginx.tmpl:ro
  letsencrypt:
    image: jrcs/letsencrypt-nginx-proxy-companion
    container_name: nginx-proxy-le
    restart: always
    depends_on:
      - nginx
      - dockergen
    environment:
      NGINX_PROXY_CONTAINER: nginx-proxy
      NGINX_DOCKER_GEN_CONTAINER: nginx-proxy-gen
    volumes:
      - conf:/etc/nginx/conf.d
      - vhost:/etc/nginx/vhost.d
      - html:/usr/share/nginx/html
      - certs:/etc/nginx/certs
      - /var/run/docker.sock:/var/run/docker.sock:ro

volumes:
  conf:
  vhost:
  html:
  certs:

networks:
  default:
    external:
      name: nginx-proxy
```

Now run

```console
you@vps:nginx-proxy-dir $ docker network create nginx-proxy
```

```console
you@vps:nginx-proxy-dir $ docker-compose up -d
```

to create a docker network called nginx-proxy and pull the required images from the Docker Hub, connecting them via the ```nginx-proxy``` network.

A quick ```docker ps``` should confirm that your containers are up and running.

This is a good moment to take a snapshot of your configuration -- you can use this as a blueprint for setting up any https services in the future.

#### Step 5: Set up Rocketchat and add it to the network
To set up Rocketchat, we need to add a MongoDB db to it (to store our data) and connect it to the ```nginx-proxy``` network so the certbot can obtain the SSL certificate for it.

In another directory, ```rocketchat-nginx-dir```, create a following ```docker-compose.yml```:

```
version: '3'

services:
  rocketchat:
    image: rocketchat/rocket.chat:latest
    restart: unless-stopped
    volumes:
      - ./uploads:/app/uploads
    environment:
      MONGO_URL: mongodb://mongo:27017/rocketchat
      ROOT_URL: http://yourdomain.com
      Accounts_UseDNsDomainCheck: "false"
      VIRTUAL_HOST: yourdomain.com
      LETSENCRYPT_HOST: yourdomain.com
      LETSENCRYPT_EMAIL: youremail@yourdomain.com
    depends_on:
      - mongo
    ports:
      - 3000:3000

  mongo:
    image: mongo:3.2
    restart: unless-stopped
    volumes:
     - ./data/db:/data/db
     - ./data/dump:/dump
    command: mongod --smallfiles --oplogSize 128 --replSet rs0

  # this container's job is just run the command to initialize the replica set.
  # it will run the command and remove himself (it will not stay running)
  mongo-init-replica:
    image: mongo:3.2
    command: 'mongo mongo/rocketchat --eval "rs.initiate({ _id: ''rs0'', members: [ { _id: 0, host: ''localhost:27017'' } ]})"'
    depends_on:
      - mongo

networks:
  default:
    external:
      name: nginx-proxy
```
Then again run

```console
you@vps:rocketchat-nginx-dir $ docker-compose up -d
```

And voila! When your new container is connected to the nginx-proxy network, it takes its VIRTUAL_HOST, LETSENCRYPT_HOST & LETSENCRYPT_EMAIL and makes a request to the certbot to obtain the SSL certificate for you. And it will keep renewing the domain for you so you don't have to worry about renewing the certificate every 90 days or so.

#### Step 6: Add A records to your domain
How this step looks largely depends on your domain service provider. What you essentially need to do is add an A record using the IP of your machine and the domain you set up in the docker-compose file.

So for instance, for subdomain.domain.com the record will be
```
SUBDOMAIN IN A [IPv4 address]
```
DNS propagation takes up to 24 hours but usually it's a matter of minutes. You can do this step before setting up the whole Docker infrastructure.

#### Step 7: Finish up Rocketchat setup and enjoy your own IM instance :)
When you first get to your newly created instance, you will be asked to create the admin account, as well as do some extra configuration. You can also set up an SMTP server (Docker-based, for instance ;)) like HogMail to set up email notifications, send invites, and more. This is however beyond the scope of this tutorial.