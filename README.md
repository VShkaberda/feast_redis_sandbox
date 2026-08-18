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
  connection_string: "172.19.0.2:6379"
auth:
    type: no_auth
EOF
```
