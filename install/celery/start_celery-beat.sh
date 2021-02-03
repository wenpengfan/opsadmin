/usr/bin/celery beat --app=opsadmin --logfile="/opt/logs/celery/beat.log" --pidfile=/opt/app/opsadmin/pid/celery-beat.pid --schedule="/opt/data/celery/celerybeat-schedule"
