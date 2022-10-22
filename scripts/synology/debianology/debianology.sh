#!/bin/bash

/usr/local/bin/docker build -t debianology . && \
/usr/local/bin/docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /volume1:/volume1 \
  -v /etc/passwd:/etc/passwd:ro \
  -v /etc/shadow:/etc/shadow:ro \
  -v /etc/group:/etc/group:ro \
  -v /etc/sudoers:/etc/sudoers:ro \
  -v /var/services/homes:/var/services/homes \
  --name debianology --hostname debianology -p 122:122 debianology
