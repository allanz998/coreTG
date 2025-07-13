#!/bin/bash
#sudo apt update && sudo apt upgrade -y
python3 -m ensurepip --upgrade
sudo apt install python3-pip
sudo apt install python3-venv
sudo apt install rabbitmq-server



#create working dir
sudo rm -rf /opt/telegram
sudo rm -rf /etc/systemd/system/chanobot.service
sudo systemctl disable chanobot 

mkdir -p /opt/telegram
cd /opt/telegram
git clone "https://github.com/allanz998/coreTG.git"
mv coreTG/* .
 


#now the rest is about launching the stuff
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt

#nohup python3 manage.py bot & nohup python3 manage.py smtp

#Bot Service
cat << EOF > /etc/systemd/system/chanobot.service
    [Unit]
    Description=Chanel posts manager
    After=network.target

    [Service]
    User=root
    Type=simple
    ExecStart=/opt/telegram/venv/bin/python3 /opt/telegram/manage.py webhook 
    WorkingDirectory=/opt/telegram
    Restart=always

    [Install]
    WantedBy=multi-user.target
EOF

sudo chmod 640 /etc/systemd/system/chanobot.service
sudo systemctl daemon-reload
sudo systemctl enable chanobot
sudo systemctl start chanobot
echo "Bot Dispatch: $(systemctl is-active chanobot)"


#Webmin Xpose


cat << EOF > /etc/systemd/system/webmin.service
    [Unit]
    Description=webmin Server logic by Olwa Inventions
    After=network.target

    [Service]
    User=root
    Type=simple
    ExecStart=/opt/telegram/venv/bin/python3 /opt/telegram/manage.py runserver 0.0.0.0:4200
    WorkingDirectory=/opt/telegram
    Restart=always

    [Install]
    WantedBy=multi-user.target
EOF

sudo chmod 640 /etc/systemd/system/webmin.service
sudo systemctl daemon-reload
sudo systemctl enable webmin
sudo systemctl start webmin
echo "DJANGO APP: $(systemctl is-active webmin)"



#celery worker


cat << EOF > /etc/systemd/system/celeryworker.service
    [Unit]
    Description=Celery logic by Olwa Inventions
    After=network.target

    [Service]
    User=root
    Type=simple
    ExecStart=/opt/telegram/venv/bin/celery -A django_tg  worker --pool=solo -l info
    WorkingDirectory=/opt/telegram
    Restart=always

    [Install]
    WantedBy=multi-user.target
EOF

sudo chmod 640 /etc/systemd/system/celeryworker.service
sudo systemctl daemon-reload
sudo systemctl enable celeryworker
sudo systemctl start celeryworker
echo "CELERY: $(systemctl is-active celeryworker)"
