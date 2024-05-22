sudo apt-get update
apt install -yq python3-pip 
pip3 install flask
nohup python3 system_init/control.py &
