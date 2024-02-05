#scripts for setting configuration
#idk anything about sh so im saving them to env variables
echo "please enter the name of your current fork(ex. Blue-Robin-Taken/MerlinLiason.git)"
echo "if you aren't looking to make any changes or don't have a fork leave it empty"
read currentFork
currentfork="git@github.com:"+=$currentFork
echo "your commits will now be made to $currentfork"
echo "how much MB of memory are you willing to allocate to your server(we reccomend 300mb for relatively chatty servers)"
read LiasonMEMORY
echo "you have allocated $LiasonMEMORY MB of memory to merlin liason"
export LiasonMEMORY
export currentfork
