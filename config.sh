#scripts for setting configuration
#idk anything about sh so im saving them to env variables
echo "please enter the name of your current fork(ex. Blue-Robin-Taken/MerlinLiason.git)"
read currentFork
currentfork="git@github.com:"+=$currentFork
echo "your commits will now be made to $currentfork"
export currentfork