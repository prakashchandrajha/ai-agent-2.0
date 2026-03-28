"""Composition Hazard Registry.

Identifies dangerous interactions when multiple concepts are used together.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class CompositionHazard:
    """Represents a dangerous interaction between multiple concepts."""
    concepts: list[str]      # Concepts that trigger this hazard when combined
    hazard: str              # What goes wrong
    mitigation: str          # How to avoid it
    severity: str            # "error" | "warning" | "note"


PYTHON_HAZARDS = [
    CompositionHazard(
        concepts=["dict iteration", "dict modification"],
        hazard="RuntimeError: dictionary changed size during iteration",
        mitigation="Use dict.copy() or list(dict.keys()) before iteration",
        severity="error"
    ),
    CompositionHazard(
        concepts=["list iteration", "list modification"],
        hazard="Skipped elements or IndexError during iteration",
        mitigation="Iterate over a copy: for item in list.copy()",
        severity="error"
    ),
    CompositionHazard(
        concepts=["file open", "exception handling"],
        hazard="Resource leak if exception raised before file.close()",
        mitigation="Always use context manager: with open(...) as f:",
        severity="warning"
    ),
    CompositionHazard(
        concepts=["mutable default argument", "function definition"],
        hazard="Mutable default shared across all calls",
        mitigation="Use None as default, create mutable inside function",
        severity="error"
    ),
    CompositionHazard(
        concepts=["float arithmetic", "equality comparison"],
        hazard="Float precision errors make == unreliable",
        mitigation="Use math.isclose() or round() for float comparison",
        severity="warning"
    ),
]

JAVASCRIPT_HAZARDS = [
    CompositionHazard(
        concepts=["array iteration", "async operation"],
        hazard="forEach doesn't await async callbacks",
        mitigation="Use for...of loop or Promise.all with .map()",
        severity="error"
    ),
    CompositionHazard(
        concepts=["object comparison", "equality check"],
        hazard="=== doesn't deep compare objects, always returns false for distinct references",
        mitigation="Use JSON.stringify() or deep equality library",
        severity="warning"
    ),
]

# Combined registry
ALL_HAZARDS = PYTHON_HAZARDS + JAVASCRIPT_HAZARDS


def check_composition_hazards(required_concepts: list[str]) -> list[CompositionHazard]:
    """Find all hazards triggered by this combination of concepts.
    
    A hazard is triggered if ALL of its required concepts are present
    (case-insensitive, substring match).
    """
    found = []
    concepts_lower = [c.lower() for c in required_concepts]
    
    for hazard in ALL_HAZARDS:
        # A hazard triggers if every concept in its 'concepts' list is matched
        # by at least one concept in the 'concepts_lower' list.
        if all(
            any(h_concept.lower() in c for c in concepts_lower)
            for h_concept in hazard.concepts
        ):
            found.append(hazard)
            
    return found
