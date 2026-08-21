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

    # User inputs
    client_id = st.number_input(
        label="Client ID",
        min_value=1,
        max_value=19,
        value=1,
        step=1,
    )

    sku_count = st.number_input(
        label="SKU Count",
        min_value=1,
        value=1,
        step=1,
    )

    if client_id is None:
        st.warning("Client ID is not provided.")
        st.stop()

    # Get client and order list for a given client_id
    orders_path = script_dir / "feature_repo/data/orders.parquet"
    entity_rows = pq.read_table(
        source=orders_path,
        columns=["client_id", "order_id"],
        filters=[("client_id", "=", client_id)],
    ).to_pylist()

    # Get data for the selected client from Feast
    features = store.get_online_features(
        features=[
            "orders_feature_view:sku_count",
            "orders_feature_view:total_price",
        ],
        entity_rows=entity_rows,
    ).to_df()

    df = pd.DataFrame.from_dict(features.to_dict())

    st.subheader("Historical data")
    st.dataframe(df)

    # Plot historical price vs SKU count
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=features["sku_count"],
            y=features["total_price"],
            mode="markers",
            name="Historical orders",
        )
    )

    X = features[["client_id", "sku_count"]]
    y_pred = model.predict(X)

    # Add prediction to the same chart
    fig.add_trace(
        go.Scatter(
            x=features["sku_count"],
            y=y_pred,
            mode="markers",
            name="Predictions",
            marker={"size": 14},
        )
    )

    fig.update_layout(
        title=f"Client {client_id}: Price vs SKU Count",
        xaxis_title="SKU Count",
        yaxis_title="Total Price",
    )

    st.plotly_chart(fig, use_container_width=True)

    # User value prediction
    st.subheader(f"Prediction for Client ID {client_id}")

    X_user = pd.DataFrame(
        {
            "client_id": [client_id],
            "sku_count": [sku_count],
        }
    )

    prediction = model.predict(X_user)[0]

    st.metric(
        label="Predicted Total Price for User Input",
        value=f"{prediction:.2f}",
    )


if __name__ == "__main__":
    main()
