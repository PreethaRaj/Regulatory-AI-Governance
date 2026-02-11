import json
import joblib
from datetime import datetime, UTC
from pathlib import Path

from src.policy import GovernancePolicy


MODEL_PATH = Path("models/model.joblib")
GOVERNANCE_PATH = Path("governance/governance.yaml")
LOG_PATH = Path("logs/inference_log.jsonl")


class InferenceService:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.policy = GovernancePolicy(GOVERNANCE_PATH)
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    def predict(self, text: str, use_case: str, requester: str):
        # 1️⃣ Enforce approved usage
        self.policy.validate_use_case(use_case)

        # 2️⃣ Model inference
        probabilities = self.model.predict_proba([text])[0]
        predicted_class = self.model.classes_[probabilities.argmax()]
        confidence = float(probabilities.max())

        # 3️⃣ Risk control
        threshold = self.policy.confidence_threshold()
        requires_human_review = confidence < threshold

        decision = {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "human_review_required": requires_human_review,
        }

        # 4️⃣ Audit log
        self._log_decision(use_case, requester, decision)

        return decision

    def _log_decision(self, use_case, requester, decision):
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "requester": requester,
            "use_case": use_case,
            "model_version": "v1.0.0",
            "decision": decision,
        }

        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")