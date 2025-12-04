"""Utilities package for bodzify_api.

This file turns `bodzify_api.utils` into a regular package (it was previously
a namespace package) to maintain backward-compatible attribute access for
submodules used by tests and third-party code (for example,
`bodzify_api.utils.audiometa_adapter`).

Avoid heavy imports here; only import submodules as needed to expose them as
attributes on the package object.
"""

# Expose commonly-used submodules as package attributes for backward compatibility
try:
    from . import audiometa_adapter  # noqa: F401
except Exception:
    # If the adapter cannot be imported (e.g., missing optional deps during tests), keep package import safe
    audiometa_adapter = None  # type: ignore

__all__ = [
    "audiometa_adapter",
]
