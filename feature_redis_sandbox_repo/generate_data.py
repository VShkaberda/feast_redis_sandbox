import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_orders_dataset(num_rows=1000):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)

    order_ids = range(1, num_rows + 1)
    client_ids = np.random.randint(1, 20, size=num_rows)
    sku_counts = np.random.randint(1, 10, size=num_rows)
    total_prices = np.round(sku_counts * np.random.uniform(10.0, 50.0, size=num_rows), 2)

    timestamps = [
        start_time + timedelta(seconds=np.random.randint(0, int((end_time - start_time).total_seconds())))
        for _ in range(num_rows)
    ]

    # 4. Create the DataFrame
    df = pd.DataFrame({
        "order_id": order_ids,
        "client_id": client_ids,
        "sku_count": sku_counts,
        "total_price": total_prices,
        "event_timestamp": pd.to_datetime(timestamps),
        "created_timestamp": pd.to_datetime(datetime.now())
    })

    os.makedirs("data", exist_ok=True)
    output_path = "data/orders.parquet"
    df.to_parquet(output_path, index=False)
    print(f"Successfully generated {num_rows} orders and saved to '{output_path}'")


if __name__ == "__main__":
    generate_orders_dataset()
