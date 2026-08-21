from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


def train_model():
    script_dir = Path(__file__).parent
    file_path = script_dir / "feature_repo" / "data" / "orders.parquet"
    df = pd.read_parquet(file_path)

    df = df.sort_values("event_timestamp")
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    cutoff = df["event_timestamp"].max() - pd.Timedelta(days=7)
    # orders are uniformly distributed for clients by date
    # hence, we can simply cut off last 7 days of the dataset
    train_df = df[df["event_timestamp"] < cutoff]
    test_df = df[df["event_timestamp"] >= cutoff]
    X_train = train_df.drop(columns=["order_id", "total_price", "event_timestamp", "created_timestamp"])
    y_train = train_df["total_price"]
    X_test = test_df.drop(columns=["order_id", "total_price", "event_timestamp", "created_timestamp"])
    y_test = test_df["total_price"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("client", OneHotEncoder(handle_unknown="ignore"), ["client_id"]),
            ("numeric", "passthrough", ["sku_count"]),
        ]
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression()),
    ])
    model.fit(X_train, y_train)

    baseline = DummyRegressor(strategy="mean")
    baseline.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²:   {r2:.3f}")
    mae_percentage = mae / test_df["total_price"].mean() * 100
    print(f"MAE: {mae_percentage:.1f}% of average order price")

    baseline_pred = baseline.predict(X_test)
    print(f"Baseline MAE: {mean_absolute_error(y_test, baseline_pred):.2f}")

    joblib.dump(model, script_dir / "model.pkl")
    print("Trained model saved to model.pkl.")


if __name__ == "__main__":
    train_model()
