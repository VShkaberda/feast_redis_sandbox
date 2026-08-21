#!/usr/bin/env python3
from datetime import timedelta

import pandas as pd
from feast import BatchFeatureView, Entity, FeatureView, Field, FileSource, Project, ValueType
from feast.aggregation import Aggregation
from feast.types import Int32, Int64, Float64

# Define a project for the feature repo
# noinspection PyArgumentList
project = Project(name="feature_redis_sandbox_repo", description="Sandbox for orders.")

# Define the source pointing directly to local files
# noinspection PyArgumentList
orders_source = FileSource(
    name="orders_source",
    path="data/orders.parquet", # Path relative to feature_store.yaml
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# noinspection PyArgumentList
city_orders_source = FileSource(
    name="clients_city_source",
    path="data/orders_clients_joined.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# Define entities
# noinspection PyArgumentList
orders_entity = Entity(name="order_id", value_type=ValueType.INT32)
# noinspection PyArgumentList
clients_entity = Entity(name="client_id", value_type=ValueType.INT32)
# noinspection PyArgumentList
cities_entity = Entity(name="city_id", value_type=ValueType.INT64)

# Define the Feature View
# noinspection PyArgumentList
orders_view = FeatureView(
    name="orders_feature_view",
    entities=[orders_entity, clients_entity],
    schema=[
        Field(name="sku_count", dtype=Int64),
        Field(name="total_price", dtype=Float64),
    ],
    source=orders_source,
    ttl=timedelta(days=90),
)

# Define the Feature View
# noinspection PyArgumentList
cities_orders_view = FeatureView(
    name="cities_orders_feature_view",
    entities=[orders_entity, clients_entity, cities_entity],
    schema=[
        Field(name="sku_count", dtype=Int64),
        Field(name="total_price", dtype=Float64),
    ],
    source=city_orders_source,
    ttl=timedelta(days=90),
)

# Define the Feature View with Aggregations
# BatchFeatureView is actually broken in v0.65.0
# and registered as FeatureView without aggregations
# noinspection PyArgumentList
# city_stats_view = BatchFeatureView(
#     name="city_stats_view",
#     entities=[cities_entity],
#     source=city_orders_source,
#     schema=[
#         Field(name="city_id", dtype=Int64),
#     ],
#     aggregations=[
#         Aggregation(
#             column="sku_count",
#             function="sum",
#             time_window=timedelta(days=30),
#         )
#     ],
#     offline=True,
#     online=True,
# )
#
# # To debug BatchFeatureView
# print(type(city_stats_view))
# print(city_stats_view.aggregations)
# print(city_stats_view.projection)
