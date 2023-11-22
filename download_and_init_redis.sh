mkdir -p data/redis

wget https://cheesegpt.s3.amazonaws.com/dump.rdb.gz -O data/redis/dump.rdb.gz
gunzip data/redis/dump.rdb.gz

docker-compose up

