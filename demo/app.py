import streamlit as st
import sys
import os

# Add the project root (one level up) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.inference import InferenceService

# Page config
st.set_page_config(
    page_title="Regulatory AI – Executive Demo",
    layout="centered"
)

st.title("Regulatory AI Classification System")
st.caption("Governed • Auditable • Human-in-the-loop")

service = InferenceService()

# ---------------------------
# Use case selection
# ---------------------------
st.subheader("1. Select Intended Use")

use_case = st.selectbox(
    "Choose how this AI will be used:",
    options=[
        "document_categorization",
        "analyst_support",
        "automated_compliance_decisions"
    ],
    format_func=lambda x: {
        "document_categorization": "Document Categorization (Approved)",
        "analyst_support": "Analyst Support (Approved)",
        "automated_compliance_decisions": "Automated Compliance Decisions (Blocked)"
    }[x]
)

# ---------------------------
# Input text
# ---------------------------
st.subheader("2. Regulatory Text")

text = st.text_area(
    "Paste a regulatory statement:",
    height=150,
    placeholder="Example: This product must comply with RoHS chemical restrictions."
)

# ---------------------------
# Run inference
# ---------------------------
if st.button("Run Classification"):
    if not text.strip():
        st.warning("Please enter regulatory text.")
    else:
        try:
            result = service.predict(
                text=text,
                use_case=use_case,
                requester="executive_demo_user"
            )

            st.success("Classification Completed")

            st.subheader("Result")
            st.write(f"**Predicted Category:** {result['predicted_class']}")
            st.write(f"**Confidence:** {int(result['confidence'] * 100)}%")

            st.subheader("Governance Controls")

            if result["human_review_required"]:
                st.warning("⚠ Human Review Required (Low Confidence)")
            else:
                st.success("✅ No Human Review Required")

            st.info("All actions have been logged for audit purposes.")

        except PermissionError as e:
            st.error("❌ Request Blocked by Governance Policy")
            st.write(str(e))

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.caption(
    "This system enforces approved AI usage, prevents misuse, "
    "and ensures regulatory auditability."
)