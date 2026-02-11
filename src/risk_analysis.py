import os
import json
import joblib
import numpy as np


# -----------------------------
# Resolve project root
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "model.joblib")
STRESS_DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "stress", "ambiguous_documents.json"
)

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "models", "risk")
LOW_CONF_PATH = os.path.join(OUTPUT_DIR, "low_confidence_predictions.json")
CONFUSION_PATH = os.path.join(OUTPUT_DIR, "confusion_pairs.json")

CONFIDENCE_THRESHOLD = 0.65


# -----------------------------
# Load artifacts
# -----------------------------
def load_model():
    return joblib.load(MODEL_PATH)


def load_stress_data():
    with open(STRESS_DATA_PATH, "r") as f:
        return json.load(f)


# -----------------------------
# Risk analysis
# -----------------------------
def analyze_risk(model, records):
    texts = [r["text"] for r in records]

    probabilities = model.predict_proba(texts)
    classes = model.classes_

    low_confidence = []
    confusion_pairs = []

    for idx, probs in enumerate(probabilities):
        sorted_idx = np.argsort(probs)[::-1]
        top_class = classes[sorted_idx[0]]
        second_class = classes[sorted_idx[1]]

        confidence_gap = probs[sorted_idx[0]] - probs[sorted_idx[1]]

        if probs[sorted_idx[0]] < CONFIDENCE_THRESHOLD:
            low_confidence.append({
                "id": records[idx]["id"],
                "text": records[idx]["text"],
                "predicted": top_class,
                "confidence": float(probs[sorted_idx[0]])
            })

        if confidence_gap < 0.15:
            confusion_pairs.append({
                "id": records[idx]["id"],
                "top_class": top_class,
                "second_class": second_class,
                "gap": float(confidence_gap)
            })

    return low_confidence, confusion_pairs


# -----------------------------
# Save artifacts
# -----------------------------
def save_outputs(low_confidence, confusion_pairs):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(LOW_CONF_PATH, "w") as f:
        json.dump(low_confidence, f, indent=2)

    with open(CONFUSION_PATH, "w") as f:
        json.dump(confusion_pairs, f, indent=2)

    print("\nRisk artifacts saved:")
    print(LOW_CONF_PATH)
    print(CONFUSION_PATH)


# -----------------------------
# Main
# -----------------------------
def main():
    print("Loading model...")
    model = load_model()

    print("Loading stress test data...")
    records = load_stress_data()

    print("Running risk analysis...")
    low_conf, confusion = analyze_risk(model, records)

    save_outputs(low_conf, confusion)


if __name__ == "__main__":
    main()