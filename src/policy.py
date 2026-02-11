import yaml


class GovernancePolicy:
    def __init__(self, governance_path: str):
        with open(governance_path, "r") as f:
            self.policy = yaml.safe_load(f)

    def validate_use_case(self, requested_use: str):
        approved = self.policy["usage"]["approved"]
        prohibited = self.policy["usage"]["prohibited"]

        if requested_use in prohibited:
            raise PermissionError(
                f"Use case '{requested_use}' is explicitly prohibited."
            )

        if requested_use not in approved:
            raise PermissionError(
                f"Use case '{requested_use}' is not in approved use cases."
            )

    def confidence_threshold(self) -> float:
        return self.policy["risk_controls"]["confidence_threshold"]

    def human_in_the_loop_required(self) -> bool:
        return self.policy["risk_controls"]["human_in_the_loop"]