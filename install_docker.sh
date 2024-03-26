#!/bin/bash

apt-get update
apt install docker.io -y
systemctl enable docker
systemctl status docker
docker run hello-world
docker ps -a
