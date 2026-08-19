# feast_redis_sandbox
Feast sandbox with Redis as online store.

## Initialization

### Dependencies

For this project the following dependencies are required:
1. Feast. Feature storage. The core of the project.
2. DuckDB. Used as offline feature storage.
3. Redis. Used as online feature storage.
4. Docker. Containerization of the project.
5. Streamlit. Framework to turn data scripts into interactive web apps.
6. Plotly. The interactive graphing library.

### Redis initialization

Create a network to connect Redis with RedisInsight :
```bash
docker network create redis-network
```

Start Redis connected to the Redis network:
```bash
docker run -d --name redis --network redis-network redis
```

To get the IP address of Redis Container: 
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis
```
This address should be used in further scripts.

### Feast initialization

Initialize Feast dir:
```bash
feast init feature_redis_sandbox_repo
cd feature_redis_sandbox_repo
mkdir data
```

Modify configuration file to combine local file storage (DuckDB)
with Docker Redis online store:
```bash
cat <<EOF > feature_redis_sandbox_repo/feature_repo/feature_store.yaml
project: feature_redis_sandbox_repo
registry: data/registry.db
provider: local
offline_store:
  type: duckdb
online_store:
  type: redis
  connection_string: "172.18.0.2:6379"
auth:
    type: no_auth
EOF
```

## Features

### Features generation

Script to generate data is `feature_redis_sandbox_repo/generate_data.py`.
`BatchFeatureView` is broken v0.65.0 and may be tested later.
After generation `*.parquet` is located in `data/` dir.
Script to generate features `feature_redis_sandbox_repo/feature_repo/features.py` should be run as
```bash
cd feature_redis_sandbox_repo/feature_repo
feast apply
```

### Materialize data into online store

To materializa data into Redis
```bash
cd feature_redis_sandbox_repo/feature_repo
feast materialize-incremental $(date +%F)
```

### Run RedisInsight to inspect Redis

Run RedisInsight in the same network as Redis
```bash
docker run -d --name redisinsight --network redis-network -p 5540:5540 redis/redisinsight:latest
```

To connect RedisInsight ot Redis add in `http://localhost:5540/`
> Alias: feast_sandbox
> 
> Host: 172.18.0.2
> 
> Port: 6379
 
To view data correctly in RedisInsight decoder should be switched to `protobuf`,
but keys and values will be still is not understandable representation.

### Get online features

To print online features for `order_id` < 20 cross joined with first 2 `client_id`:
```bash
cd feature_redis_sandbox_repo/feature_repo
python ./get_online_features.py
```
