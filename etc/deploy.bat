git commit -am %1s
git push
ssh root@williamgowell.com "cd ~/slack-does-chores && git stash && git pull && git stash drop -q | true && sed -i 's/\r//' *.sh && chmod +x etc/run.sh && ./etc/run.sh"
