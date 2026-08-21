#!/usr/bin/env python3
import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


def generate_orders_dataset(num_rows=1000):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)

    order_ids = range(1, num_rows + 1)
    client_ids = np.random.randint(1, 20, size=num_rows)
    city_ids = [1] * 14 + [2] * 4 + [3] * 1
    np.random.shuffle(city_ids)
    sku_counts = np.random.randint(1, 10, size=num_rows)
    total_prices = np.round(sku_counts * np.random.uniform(10.0, 50.0, size=num_rows), 2)

    timestamps = [
        start_time + timedelta(seconds=np.random.randint(0, int((end_time - start_time).total_seconds())))
        for _ in range(num_rows)
    ]

    # 4. Create the DataFrame
    df_orders = pd.DataFrame({
        "order_id": order_ids,
        "client_id": client_ids,
        "sku_count": sku_counts,
        "total_price": total_prices,
        "event_timestamp": pd.to_datetime(timestamps),
        "created_timestamp": pd.to_datetime(datetime.now()),
    })

    df_cities = pd.DataFrame({
        "client_id": range(1, 20),
        "city_id": city_ids,
    })

    df_joined = df_orders.merge(
        df_cities,
        on=["client_id"],
        how="inner",
    )

    os.makedirs("feature_repo/data", exist_ok=True)
    output_path_orders = "feature_repo/data/orders.parquet"
    df_orders.to_parquet(output_path_orders, index=False)
    output_path_cities = "feature_repo/data/clients.parquet"
    df_cities.to_parquet(output_path_cities, index=False)
    output_path_joined = "feature_repo/data/orders_clients_joined.parquet"
    df_joined.to_parquet(output_path_joined, index=False)
    print(f"Successfully generated {num_rows} orders, clients and joined df.")


if __name__ == "__main__":
    generate_orders_dataset()
