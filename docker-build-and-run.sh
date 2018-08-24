#!/bin/sh

set -e

docker build -t istepanov/vgg-traffic-lights .
docker run --runtime=nvidia -ti --rm -v `pwd`:/src istepanov/vgg-traffic-lights bash
