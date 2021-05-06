#!/usr/bin/env bash
set -e

# Always update this if you made changes to the Dockerfile
TAG=$(git describe)

buildah bud \
    -t "cselab/korali:${TAG}" \
    -t "cselab/korali:latest" .

podman login docker.io
podman push "cselab/korali:${TAG}"
podman push "cselab/korali:latest"

podman rmi -f cselab/korali:${TAG}
