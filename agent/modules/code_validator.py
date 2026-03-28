import re
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_safe: bool
    violations: list[str]
    suggestion: str

DANGEROUS_PATTERNS = [
    (r'\bimport\s+os\b',          "os module — filesystem access"),
    (r'\bimport\s+subprocess\b',  "subprocess — shell execution"),
    (r'\bimport\s+sys\b',         "sys — interpreter access"),
    (r'\b__import__\b',           "dynamic import bypass"),
    (r'\bopen\s*\(',              "file I/O"),
    (r'\bexec\s*\(',              "exec() — arbitrary code"),
    (r'\beval\s*\(',              "eval() — arbitrary expression"),
    (r'\bglobals\s*\(',           "globals() — scope escape"),
    (r'\bsocket\b',               "network socket"),
    (r'\burllib\b|\brequests\b',  "HTTP client"),
    (r'\bshutil\b',               "file operations"),
    (r'\bpickle\b',               "deserialization attack vector"),
    (r'\b__builtins__\b',         "builtins access"),
    (r'compile\s*\(',             "compile() — code generation"),
]

def validate_code(code: str) -> ValidationResult:
    """Perform static analysis on code to detect dangerous patterns.
    
    Returns a ValidationResult indicating safety and any violations found.
    """
    violations = []
    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            violations.append(description)
    
    is_safe = len(violations) == 0
    suggestion = "Remove dangerous patterns. Only use pure Python data structures and algorithms." if violations else ""
    
    return ValidationResult(is_safe=is_safe, violations=violations, suggestion=suggestion)
