#!/bin/bash
set -e

cd /opt/app/opsadmin
python manage.py makemigrations
python manage.py migrate

systemctl daemon-reload
systemctl start redis.service
systemctl start opsadmin.service
systemctl start celery.service
systemctl start nginx.service
