echo "\$nrconf{kernelhints} = 0;" >> /etc/needrestart/needrestart.conf
echo "\$nrconf{restart} = 'l';" >> /etc/needrestart/needrestart.conf
sudo apt-get update
apt install -yq python3-pip 
pip3 install flask
pip3 install apscheduler
pip3 install requests
# 打开防火墙
yes | sudo ufw enable
yes | sudo ufw allow 80/tcp
yes | sudo ufw allow ssh
yes | sudo ufw reload
cd ~

echo '[Unit]
Description=Your Control Service
After=network.target

[Service]
Type=simple
ExecStart=nohup python3 /root/system_init/control.py &
Restart=always

[Install]
WantedBy=multi-user.target'> /etc/systemd/system/control.service
sudo systemctl enable control.service
sudo systemctl start control.service



