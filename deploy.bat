echo $1
git commit -am "teste"
git push
ssh root@williamgowell.com "cd ~/slack-does-chores && git pull && ./run.sh"
