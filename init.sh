echo "\$nrconf{kernelhints} = 0;" >> /etc/needrestart/needrestart.conf
echo "\$nrconf{restart} = 'l';" >> /etc/needrestart/needrestart.conf
sudo apt-get update
apt install -yq python3-pip 
pip3 install flask
pip3 install apscheduler
pip3 install requests
# 打开防火墙
sudo ufw enable
sudo ufw allow 80/tcp
sudo ufw allow ssh
sudo ufw reload
cd ~
nohup python3 system_init/control.py &
