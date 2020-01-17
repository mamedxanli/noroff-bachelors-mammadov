#!/bin/sh

# Set variables
_now=$(date +"%m_%d_%Y")
_file="auth_$_now.log"

#copy files from the container to host
docker cp 4b99:/var/log/auth.log /home/coach/workspace/noroff-bachelors-mammadov/data/$_file
