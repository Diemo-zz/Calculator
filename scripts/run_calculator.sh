docker build -t calculator:latest .

export HOST_SUBDOMAIN=futurice.diarmaiddeburca.com

docker stack deploy -c docker-compose.yml calc