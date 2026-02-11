# Regulatory-AI-Governance

Governed NLP system for regulatory document classification with audit-ready, policy-enforced AI.

This project demonstrates how to combine ML, governance, and auditability in a practical regulatory AI system.


\# Regulatory AI Classification System



\*\*Description:\*\*  

This project implements a \*\*governed NLP system\*\* for classifying regulatory documents. It combines interpretable machine learning with \*\*policy-enforced, audit-ready AI\*\*, ensuring safe and compliant use in regulated environments.



---



\##  Key Features



\- \*\*Synthetic \& versioned datasets\*\* for reproducible experiments

\- \*\*Interpretable NLP classification model\*\* (TF-IDF + Logistic Regression)

\- \*\*Explainability \& risk analysis\*\* for each prediction

\- \*\*Governance \& model card\*\*: links dataset versions to model versions, defines approved use cases, and enforces risk controls

\- \*\*Policy-enforced inference\*\*: automatically blocks prohibited use, triggers human review for low-confidence predictions, and logs all actions

\- \*\*Audit-ready logging\*\*: every decision is recorded for regulatory traceability

\- \*\*Executive demo UI\*\*: simple, non-technical interface to demonstrate safe AI usage



---



\##  Project Structure

Reg-pj/

├── data/ # Synthetic dataset

├── models/ # Trained ML model

├── governance/ # Model card, approvals, policies

├── logs/ # Inference audit logs

├── src/ # Python source code (data prep, training, inference)

└── demo/ # Streamlit demo UI for executive presentation



---



\## How to Run


1\. \*\*Create and activate a virtual environment\*\*



From Command Prompt:

python -m venv venv

venv\\Scripts\\activate       # Windows



streamlit run demo/app.py

