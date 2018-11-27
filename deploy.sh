#!/usr/bin/env bash

git commit -am "$1"
git push
ssh root@williamgowell.com -C "cd ~/slack-does-chores && git pull && ./run.sh"
