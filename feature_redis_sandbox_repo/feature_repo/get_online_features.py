#!/usr/bin/env python3
from feast import FeatureStore
import pandas as pd


def main(num_rows=20):
    store = FeatureStore(repo_path=".")

    client_ids = range(1, 3)
    order_ids = range(1, num_rows + 1)
    city_ids = range(1, 3)

    feature_vector_orders = store.get_online_features(
        features=[
            "orders_feature_view:sku_count",
            "orders_feature_view:total_price"
        ],
        entity_rows=[{"client_id": cid, "order_id": oid} for cid in client_ids for oid in order_ids],
    )

    df = pd.DataFrame.from_dict(feature_vector_orders.to_dict())
    df = df[["order_id", "client_id", "sku_count", "total_price"]]
    print(df)

    # Broken in v0.65.0
    # fv = store.get_feature_view("city_stats_view")
    #
    # print(fv)
    # print("features:")
    #
    # for feature in fv.features:
    #     print(f"  {feature.name}: {feature.dtype}")
    #
    # feature_vector_cities = store.get_online_features(
    #     features=[
    #         "city_stats_view:sku_count_30d",
    #     ],
    #     entity_rows=[{"city_id": city_id} for city_id in city_ids],
    # )
    #
    # df = pd.DataFrame.from_dict(feature_vector_cities.to_dict())
    # df = df[["city_id", "sku_count_7d"]]
    # print(df)


if __name__ == "__main__":
    main()
