import os
import json
import random
import uuid
from datetime import datetime, timezone
from typing import List, Dict

# -----------------------------
# Global configuration
# -----------------------------
RANDOM_SEED = 42
NUM_DOCUMENTS = 200
VERSIONS_PER_DOC = 3

BASE_DIR = "data"
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
VERSION_DIR = os.path.join(BASE_DIR, "versions")

random.seed(RANDOM_SEED)

# -----------------------------
# Regulatory domains
# -----------------------------
DOMAINS = {
    "PRODUCT_SAFETY": [
        "must meet mechanical safety standards",
        "shall not pose a risk to users",
        "requires safety certification before sale",
    ],
    "ENVIRONMENTAL": [
        "must comply with environmental protection norms",
        "requires waste reduction measures",
        "environmental impact must be documented",
    ],
    "WIRELESS_EMC": [
        "shall operate within electromagnetic emission limits",
        "must not cause radio interference",
        "compliance with EMC standards is required",
    ],
    "ENERGY_EFFICIENCY": [
        "must meet minimum energy efficiency ratings",
        "power consumption shall not exceed limits",
        "energy usage must be optimized",
    ],
    "CHEMICAL_RESTRICTION": [
        "restricted substances shall not exceed thresholds",
        "use of hazardous chemicals is prohibited",
        "chemical composition must be disclosed",
    ],
}

EFFECTIVE_DATES = [
    "2023-01-01",
    "2024-01-01",
    "2025-06-01",
]

# -----------------------------
# Utility functions
# -----------------------------
def ensure_dirs():
    for d in [RAW_DIR, PROCESSED_DIR, VERSION_DIR]:
        os.makedirs(d, exist_ok=True)


def generate_base_text(domain: str) -> str:
    clause = random.choice(DOMAINS[domain])
    date = random.choice(EFFECTIVE_DATES)
    return (
        f"This regulation applies to products sold globally. "
        f"The product {clause}. "
        f"Effective date: {date}."
    )


def mutate_text(text: str) -> str:
    """Simulate regulation updates by small wording changes"""
    mutations = [
        ("must", "shall"),
        ("shall", "must"),
        ("globally", "internationally"),
        ("requires", "mandates"),
    ]
    old, new = random.choice(mutations)
    return text.replace(old, new, 1)


# -----------------------------
# Schema validation
# -----------------------------
REQUIRED_FIELDS = {
    "document_id": str,
    "version": int,
    "domain": str,
    "text": str,
    "effective_date": str,
    "created_at": str,
}


def validate_schema(record: Dict):
    for field, field_type in REQUIRED_FIELDS.items():
        if field not in record:
            raise ValueError(f"Missing field: {field}")
        if not isinstance(record[field], field_type):
            raise TypeError(f"Field {field} has wrong type")


# -----------------------------
# Data generation
# -----------------------------
def generate_documents() -> List[Dict]:
    documents = []

    for _ in range(NUM_DOCUMENTS):
        document_id = str(uuid.uuid4())
        domain = random.choice(list(DOMAINS.keys()))
        base_text = generate_base_text(domain)

        for version in range(1, VERSIONS_PER_DOC + 1):
            text = base_text if version == 1 else mutate_text(base_text)

            record = {
                "document_id": document_id,
                "version": version,
                "domain": domain,
                "text": text,
                "effective_date": random.choice(EFFECTIVE_DATES),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

            validate_schema(record)
            documents.append(record)

    return documents


# -----------------------------
# Save datasets
# -----------------------------
def save_data(documents: List[Dict]):
    # Save raw full dataset
    raw_path = os.path.join(RAW_DIR, "regulatory_documents.json")
    with open(raw_path, "w") as f:
        json.dump(documents, f, indent=2)

    # Save processed version (latest versions only)
    latest_docs = {}
    for doc in documents:
        doc_id = doc["document_id"]
        if (
            doc_id not in latest_docs
            or doc["version"] > latest_docs[doc_id]["version"]
        ):
            latest_docs[doc_id] = doc

    processed_path = os.path.join(PROCESSED_DIR, "latest_documents.json")
    with open(processed_path, "w") as f:
        json.dump(list(latest_docs.values()), f, indent=2)

    # Save version metadata
    version_meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "num_documents": NUM_DOCUMENTS,
        "versions_per_document": VERSIONS_PER_DOC,
        "random_seed": RANDOM_SEED,
    }

    version_path = os.path.join(VERSION_DIR, "dataset_metadata.json")
    with open(version_path, "w") as f:
        json.dump(version_meta, f, indent=2)


# -----------------------------
# Main
# -----------------------------
def main():
    ensure_dirs()
    documents = generate_documents()
    save_data(documents)
    print(f"Generated {len(documents)} regulatory document records")


if __name__ == "__main__":
    main()