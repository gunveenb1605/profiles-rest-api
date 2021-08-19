#!/usr/bin/env bash
#This will run always after the setup script whenever anything new is added to the app in github
set -e

PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'

git pull
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart profiles_api

echo "DONE! :)"
