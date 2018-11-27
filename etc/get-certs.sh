#!/usr/bin/env bash
docker-compose run --rm letsencrypt \
  letsencrypt certonly --webroot \
  --email owner@bookingsgolf.com --agree-tos \
  -w /var/www/letsencrypt -d bookingsgolf.com
docker-compose kill -s SIGHUP proxy
