#!/bin/bash
# ref: https://askubuntu.com/questions/425754/how-do-i-run-a-sudo-command-inside-a-script
if ! [ $(id -u) = 0 ]; then
   echo "The script need to be run as root." >&2
   exit 1
fi

if [ $SUDO_USER ]; then
    real_user=$SUDO_USER
else
    real_user=$(whoami)
fi

apt-get update
apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt-cache policy docker-ce
apt install docker-ce -y
curl -L https://github.com/docker/compose/releases/download/1.26.2/docker-compose-`uname
-s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

sudo -u $real_user git clone https://github.com/Diemo-zz/Calculator.git

cd  Calculator
docker build -t calculator:latest .

docker swarm init
docker swarm join-token manager

docker network create --driver=overlay traefik-public

docker volume create traefik-public-certificates

export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}')

docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID

export USERNAME=admin
export PASSWORD=myfuturicepassword
export EMAIL=diarmaiddeburca@gmail.com
export TRAEFIK_SUBDOMAIN=traefik.diarmaiddeburca.com
export HOST_SUBDOMAIN=futurice.diarmaiddeburca.com
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

docker stack deploy -c app/traefik.yml traefik
docker stack deploy -c docker-compose.yml calc
