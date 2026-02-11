import os
import json
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


# -----------------------------
# Resolve project root
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed", "latest_documents.json"
)

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

RANDOM_STATE = 42
TEST_SIZE = 0.2


# -----------------------------
# Load data
# -----------------------------
def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    with open(DATA_PATH, "r") as f:
        records = json.load(f)

    df = pd.DataFrame(records)

    required_columns = {"text", "domain"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain columns: {required_columns}"
        )

    return df


# -----------------------------
# Build model pipeline
# -----------------------------
def build_pipeline():
    pipeline = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=5000,
                    stop_words="english",
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    solver="lbfgs",
                    random_state=RANDOM_STATE,
                    max_iter=1000,
                ),
            ),
        ]
    )
    return pipeline


# -----------------------------
# Train & evaluate
# -----------------------------
def train_model(df):
    X = df["text"]
    y = df["domain"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = build_pipeline()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model


# -----------------------------
# Save model artifact
# -----------------------------
def save_model(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")


# -----------------------------
# Main
# -----------------------------
def main():
    print("Loading data...")
    df = load_data()

    print("Training model...")
    model = train_model(df)

    print("Saving model...")
    save_model(model)


if __name__ == "__main__":
    main()