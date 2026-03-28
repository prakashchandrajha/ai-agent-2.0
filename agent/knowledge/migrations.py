"""EKU Schema Migrations.

Handles upgrading old EKU data formats to the current version.
"""

from typing import Any

SCHEMA_VERSION = "2.0.0"

def migrate_eku(data: dict[str, Any]) -> dict[str, Any]:
    """Migrate EKU data to the latest version."""
    # Check for old 'version' int or missing version
    version = data.get("_schema_version")
    if not version:
        version = data.get("version", 1)
    
    if version == 1 or version == "1.0.0":
        data = _migrate_v1_to_v2(data)
    
    return data

def _migrate_v1_to_v2(data: dict[str, Any]) -> dict[str, Any]:
    """Upgrade EKU from version 1 to version 2.0.0."""
    # New fields in v2 with their defaults
    v2_fields = {
        "confidence_breakdown": {},
        "hard_constraints": [],
        "soft_constraints": [],
        "violated_constraints_log": [],
        "canonical_traces": [],
        "trace_patterns": [],
        "prediction_accuracy": 0.0,
        "prediction_history": [],
        "confusion_gaps": [],
        "micro_skills": [],
        "last_used_timestamp": "",
        "usage_count": 0,
        "decay_score": 0.0,
        "state_sensitive": False,
        "context_dependencies": [],
        "avg_robustness_score": 1.0,
        "fragility_flags": [],
        "source_urls": [],
        "avg_source_authority": 0.0,
        "mastery_criteria_met": [],
        "mastery_criteria_unmet": [],
        "gate_diagnostics": [],
        "version_bounds": {},
        "context_fingerprint": {},
    }

    for field, default in v2_fields.items():
        if field not in data:
            data[field] = default
    
    # Remove old version field if it exists
    if "version" in data:
        del data["version"]
        
    data["_schema_version"] = SCHEMA_VERSION
    return data
