# Model Card — Regulatory Text Classification Model

## 1. Model Overview

**Model Name:** Regulatory Text Classifier  
**Model Version:** v1.0.0  
**Model Type:** TF-IDF + Logistic Regression (multiclass)  
**Owner Team:** AI / Regulatory Engineering  
**Human-in-the-loop:** Required

---

## 2. Intended Use

### Approved Use Cases
- Regulatory document categorization
- Compliance document triage
- Analyst decision support
- Routing documents to subject-matter experts

### Explicitly Not Approved
- Automated compliance approval or rejection
- Legal decision-making
- Regulatory certification
- Customer-facing enforcement actions

---

## 3. Training Data

**Dataset Name:** Synthetic Regulatory Text Dataset  
**Dataset Version:** v1.0.0  
**Number of Records:** 600  
**Data Type:** Synthetic, English-only regulatory text  
**Source:** Programmatically generated (data_prep.py)

**Label Classes:**
- CHEMICAL_RESTRICTION
- ENERGY_EFFICIENCY
- ENVIRONMENTAL
- PRODUCT_SAFETY
- WIRELESS_EMC

---

## 4. Dataset → Model Lineage

| Artifact | Identifier |
|--------|------------|
| Dataset Version | v1.0.0 |
| Dataset Hash | Generated during data prep |
| Training Script | train.py |
| Model Artifact | models/regulatory_model.joblib |

This model **must not** be retrained on unversioned or undocumented datasets.

---

## 5. Performance Summary

- Overall Accuracy: ~100% (synthetic dataset)
- Evaluation Method: Hold-out test set
- Explainability: Class-wise top TF-IDF features extracted

⚠ Performance reflects **synthetic data only** and does not guarantee real-world accuracy.

---

## 6. Explainability & Transparency

- Global explainability via top TF-IDF features per class
- No black-box components
- Model behavior is fully inspectable

Artifacts:
- `artifacts/top_features.json`
- `artifacts/confusion_matrix.png`

---

## 7. Known Limitations

- Trained on synthetic data only
- Not validated on real regulatory documents
- English-language text only
- Single-label classification
- Sensitive to vocabulary drift

---

## 8. Risk Assessment

### Identified Risks
- Misclassification of ambiguous documents
- Overconfidence due to clean synthetic data
- Vocabulary drift in real-world data

### Risk Mitigations
- Human review for low-confidence predictions
- Periodic retraining with updated datasets
- Confidence threshold enforcement

---

## 9. Ethical & Compliance Considerations

- No personal data used
- No protected attributes involved
- Model does not make autonomous decisions
- Designed for assistive use only

---

## 10. Approval Status

**Model Status:** Approved for internal analytical use  
**Approval Authority:** Regulatory AI Review Board  
**Approval Date:** YYYY-MM-DD  

Re-approval required upon:
- Dataset change
- Model architecture change
- Deployment context change