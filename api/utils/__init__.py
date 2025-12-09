"""Utilities package for api.

This file turns `api.nto a regular package (it was previously
a namespace package) to maintain backward-compatible attribute access for
submodules used by tests and third-party code (for example,
`api.adapter`).

Avoid heavy imports here; only import submodules as needed to expose them as
attributes on the package object.
"""

__all__ = []
