#!/bin/bash
set -e

read -p "Database IP: " db_ip
read -p "Database User: " db_user
read -p "Database Password: " db_pwd

app_dir="/opt/app/opsadmin/"
mkdir -p $app_dir/pid
mkdir -p $app_dir/bin

data_dir="/opt/data/celery/"
mkdir -p $data_dir

cd $app_dir/install
cp nginx/opsadmin.conf /etc/nginx/conf.d/
cp opsadmin/start_opsadmin.sh $app_dir/bin/
if [ ! -f $app_dir/opsadmin.conf ];then
    cp opsadmin/opsadmin.conf $app_dir
fi
cp opsadmin/opsadmin.service /usr/lib/systemd/system
cp celery/start_celery-worker.sh $app_dir/bin
cp celery/stop_celery-worker.sh $app_dir/bin
cp celery/start_celery-beat.sh $app_dir/bin
cp celery/stop_celery-beat.sh $app_dir/bin
cp celery/celery-worker.service /usr/lib/systemd/system
cp celery/celery-beat.service /usr/lib/systemd/system

yum -y install $(cat rpm_requirements.txt)
pip install -r requirements.txt

cd $app_dir
find . -name "*.pyc" -delete

/usr/bin/mysql -h$db_ip -u$db_user -p$db_pwd -e "CREATE DATABASE IF NOT EXISTS testdb DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"
sed -i 's/NAMES = AppOwner.objects.values_list(\"id\", \"name\")/NAMES = \"\"/g' accounts/forms.py
python manage.py makemigrations accounts
python manage.py makemigrations appconf
python manage.py makemigrations cmdb
python manage.py makemigrations config
python manage.py makemigrations navi
python manage.py makemigrations orders
python manage.py makemigrations tests
python manage.py makemigrations workload
python manage.py migrate
sed -i 's/NAMES = \"\"/NAMES = AppOwner.objects.values_list(\"id\", \"name\")/g' accounts/forms.py

/usr/bin/mysql -h$db_ip -u$db_user -p$db_pwd -e 'insert into opsadmin.accounts_userinfo(password,username,email,is_active,is_superuser,is_staff,ldap_name) values ("pbkdf2_sha256$36000$lI6DZONijv9q$jzJtbIuKz3kj9kBRkfNW832iAXznV5WxDqTrmhmA6Tc=","admin","admin@163.com",1,1,0,"");'

systemctl enable redis.service
systemctl enable opsadmin.service
systemctl enable celery-worker.service
systemctl enable celery-beat.service
systemctl enable nginx.service
