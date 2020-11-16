/usr/bin/celery multi start node1 node2 --concurrency=2 --app=opsadmin --logfile="/opt/logs/celery/worker-%n%I.log" --pidfile=/opt/app/opsadmin/pid/celery-worker-%n.pid
