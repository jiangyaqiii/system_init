sudo apt-get update
apt install -yq python3-pip 
pip3 install flask
pip3 install apscheduler
pip3 install requests
nohup python3 system_init/control.py &
