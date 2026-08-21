from pathlib import Path

import joblib
import pandas as pd
import pyarrow.parquet as pq
import plotly.graph_objects as go
import streamlit as st
from feast import FeatureStore


def main():
    script_dir = Path(__file__).parent
    feature_repo_path = script_dir / "feature_repo"
    store = FeatureStore(repo_path=str(feature_repo_path))
    model = joblib.load(script_dir / "model.pkl")

    st.title("Client Price by Sku Count Prediction")

    client_id = st.number_input(
        label="Client ID",
        min_value=1,
        max_value=19,
        value=1,
        step=1,
    )

    if client_id is None:
        st.warning("Client ID is not provided.")
        st.stop()

    # get client and order list for a given client_id
    orders_path = script_dir / "feature_repo/data/orders.parquet"
    entity_rows = pq.read_table(
        source=orders_path,
        columns=["client_id", "order_id"],
        filters=[("client_id", "=", client_id)],
    ).to_pylist()

    features = store.get_online_features(
        features=[
            "orders_feature_view:sku_count",
            "orders_feature_view:total_price",
        ],
        entity_rows=entity_rows,
    ).to_df()

    df = pd.DataFrame.from_dict(features.to_dict())

    st.subheader("Features extracted:")
    st.dataframe(df)

    X = features[["client_id", "sku_count"]]
    y_pred = model.predict(X)

    st.subheader(f"Prediction for Client ID {client_id}")
    st.write(f"Total Price Prediction: **{y_pred}**")

if __name__ == "__main__":
    main()
