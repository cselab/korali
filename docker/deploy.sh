#!/usr/bin/env bash
set -e

# Always update this if you made changes to the Dockerfile
TAG=$(git describe)

docker build -f Dockerfile \
    -t "cselab/korali:${TAG}" \
    -t "cselab/korali:latest" .

docker login
docker push "cselab/korali:${TAG}"
docker push "cselab/korali:latest"

docker rmi -f cselab/korali:${TAG}
