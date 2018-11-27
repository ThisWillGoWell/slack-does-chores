#!/usr/bin/env bash
echo $1
git commit -am "$1"
git push
ssh root@williamgowell.com -C "cd ~/slack-does-chores && git pull && ./run.sh"
