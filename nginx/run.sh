#!/bin/bash

docker run -p 8080:8080 -v /home/rp/projects/python/rabbitmq/nginx/nginx.conf:/etc/nginx/nginx.conf:ro nginx