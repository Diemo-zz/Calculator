docker swarm init
docker swarm join-token manager

docker network create --driver=overlay traefik-public

docker volume create traefik-public-certificates

export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}')

docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID

export USERNAME=$USERNAME
export EMAIL=diarmaiddeburca@gmail.com
export TRAEFIK_SUBDOMAIN=traefik.diarmaiddeburca.com
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

docker stack deploy -c app/traefik.yml traefik