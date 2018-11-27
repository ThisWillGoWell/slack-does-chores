git commit -am %1s
git push
ssh root@williamgowell.com "cd ~/slack-does-chores && git pull && ./run.sh"
