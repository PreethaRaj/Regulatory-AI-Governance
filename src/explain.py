import os
import json
import joblib
import numpy as np


# -----------------------------
# Resolve project root
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "model.joblib")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "models", "explainability")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "top_features_per_class.json")

TOP_K = 15


# -----------------------------
# Load trained model
# -----------------------------
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found. Run train.py first.")

    return joblib.load(MODEL_PATH)


# -----------------------------
# Extract top features
# -----------------------------
def extract_top_features(model, top_k=TOP_K):
    tfidf = model.named_steps["tfidf"]
    clf = model.named_steps["clf"]

    feature_names = np.array(tfidf.get_feature_names_out())
    class_labels = clf.classes_

    explanations = {}

    for idx, class_name in enumerate(class_labels):
        class_coefficients = clf.coef_[idx]

        top_positive_idx = np.argsort(class_coefficients)[-top_k:][::-1]

        explanations[class_name] = [
            {
                "term": feature_names[i],
                "weight": float(class_coefficients[i])
            }
            for i in top_positive_idx
        ]

    return explanations


# -----------------------------
# Save explainability artifact
# -----------------------------
def save_explanations(explanations):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(explanations, f, indent=2)

    print(f"\nExplainability artifact saved to:\n{OUTPUT_PATH}")


# -----------------------------
# Main
# -----------------------------
def main():
    print("Loading model...")
    model = load_model()

    print("Extracting top features per class...")
    explanations = extract_top_features(model)

    print("Saving explainability artifact...")
    save_explanations(explanations)


if __name__ == "__main__":
    main()