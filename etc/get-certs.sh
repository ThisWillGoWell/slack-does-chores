#!/usr/bin/env bash
docker-compose run --rm letsencrypt \
  letsencrypt certonly --webroot \
  --email will@williamgowell.com --agree-tos \
  -w /var/www/letsencrypt -d williamgowell.com
docker-compose kill -s SIGHUP proxy
