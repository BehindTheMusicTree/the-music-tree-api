from dataclasses import dataclass, field
from typing import Any, Dict, Union


def default_error_code() -> str:
    return "error"


@dataclass
class ErrorDetail:
    message: str
    code: str = field(default_factory=default_error_code)
    details: Union[Dict[str, Any], None] = None

    def __post_init__(self) -> None:
        # If None code is explicitly provided, set it to default to ensure consistency
        if self.code is None:
            self.code = default_error_code()
