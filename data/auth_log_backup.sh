_now=$(date +"%m_%d_%Y")
_file="auth_$_now.log"
docker cp 4d:/var/log/auth.log /home/coach/workspace/noroff_bachelors/data/$_file
