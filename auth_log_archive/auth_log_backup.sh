_now=$(date +"%m_%d_%Y")
_file="auth_$_now.log"
docker cp 57:/var/log/auth.log /home/coach/workspace/noroff_bachelors/auth_log_archive/$_file
