from src.inference import InferenceService

service = InferenceService()

print("=== Approved usage ===")
result = service.predict(
    text="This product must comply with RoHS chemical restrictions.",
    use_case="document_categorization",
    requester="compliance_analyst_01"
)
print(result)

print("\n=== Prohibited usage ===")
try:
    service.predict(
        text="This device is approved for market release.",
        use_case="automated_compliance_decisions",
        requester="system_bot"
    )
except PermissionError as e:
    print("Blocked:", e)