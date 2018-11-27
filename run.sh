#!/usr/bin/env bash
. $(pwd)/secrets.env
docker-compose build
docker-compose up -d
docker-compose logs -f
