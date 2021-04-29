#!/usr/bin/env bash
set -e
docker rmi -f cselab/korali:latest
docker build -f Dockerfile -t 'cselab/korali:latest' .
