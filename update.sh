git init
git remote add origin git@github.com:Blue-Robin-Taken/MerlinLiason.git
git reset --hard HEAD
git pull git@github.com:Blue-Robin-Taken/MerlinLiason.git
#what if the person that pulls isnt you???
#probably should add a config file or notice
chmod u+x setPermissions.sh
chmod u+x update.sh
./setPermissions.sh
echo "updated"
