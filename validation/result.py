from dataclasses import dataclass


@dataclass
class ValidationResult:
    passed: bool
    name: str
    message: str