#!/usr/bin/env python3
"""
Analyze codebase to identify shared code components for repository splitting.

Usage:
    python scripts/analyze-shared-code.py [--output output.json]
"""

import ast
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import click


class ImportAnalyzer(ast.NodeVisitor):
    """AST visitor to extract imports from Python files."""

    def __init__(self):
        self.imports = []
        self.from_imports = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            module = node.module
            for alias in node.names:
                self.from_imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)


def analyze_file(file_path: Path) -> dict[str, Any]:
    """Analyze a Python file for imports and exports."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(file_path))
        analyzer = ImportAnalyzer()
        analyzer.visit(tree)

        return {
            "path": str(file_path),
            "imports": analyzer.imports,
            "from_imports": analyzer.from_imports,
            "lines": len(content.splitlines()),
        }
    except Exception as e:
        return {
            "path": str(file_path),
            "error": str(e),
        }


def find_python_files(directory: Path) -> list[Path]:
    """Find all Python files in directory, excluding __pycache__ and test files."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                # Optionally exclude test files
                # if "test" not in str(file_path):
                python_files.append(file_path)

    return python_files


def build_dependency_graph(analyses: list[dict]) -> dict[str, Any]:
    """Build a dependency graph from file analyses."""
    # Map module paths to their analyses
    module_map = {}
    for analysis in analyses:
        if "error" not in analysis:
            path = analysis["path"]
            # Convert file path to module path
            module_path = path.replace("/", ".").replace(".py", "")
            if module_path.startswith("bodzify_api."):
                module_map[module_path] = analysis

    # Build dependency graph
    graph = {}
    for module_path, analysis in module_map.items():
        dependencies = set()

        # Add imports
        for imp in analysis.get("imports", []):
            if imp.startswith("bodzify_api."):
                dependencies.add(imp)

        # Add from imports
        for from_imp in analysis.get("from_imports", []):
            if from_imp.startswith("bodzify_api."):
                # Extract module from "module.Class"
                dep_module = ".".join(from_imp.split(".")[:-1])
                dependencies.add(dep_module)

        if dependencies:
            graph[module_path] = {
                "dependencies": list(dependencies),
                "lines": analysis.get("lines", 0),
            }

    return graph


def find_shared_components(graph: dict[str, Any], min_dependents: int = 3) -> dict[str, Any]:
    """Find components that are used by multiple other components."""
    # Count how many modules depend on each module
    dependent_count = defaultdict(int)
    dependents = defaultdict(list)

    for module, data in graph.items():
        for dep in data.get("dependencies", []):
            dependent_count[dep] += 1
            dependents[dep].append(module)

    # Find modules with many dependents
    shared = {}
    for module, count in dependent_count.items():
        if count >= min_dependents:
            shared[module] = {
                "dependent_count": count,
                "dependents": dependents[module],
                "lines": graph.get(module, {}).get("lines", 0),
            }

    return shared


def categorize_component(module_path: str) -> str:
    """Categorize a component based on its path."""
    if "model/base" in module_path:
        return "core_infrastructure"
    elif "exception" in module_path:
        return "core_infrastructure"
    elif "middleware" in module_path:
        return "core_infrastructure"
    elif "filtering/backend" in module_path:
        return "core_infrastructure"
    elif "utils" in module_path:
        return "utility"
    elif "serializer" in module_path and "AppInputSerializer" in module_path:
        return "core_infrastructure"
    elif "model" in module_path:
        return "domain_model"
    elif "view" in module_path:
        return "domain_view"
    elif "serializer" in module_path:
        return "domain_serializer"
    else:
        return "other"


@click.command()
@click.option(
    "--directory",
    default="bodzify_api",
    help="Directory to analyze",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--output",
    default="shared-code-analysis.json",
    help="Output JSON file",
    type=click.Path(path_type=Path),
)
@click.option(
    "--min-dependents",
    default=3,
    help="Minimum number of dependents to consider a component 'shared'",
    type=int,
)
def main(directory: Path, output: Path, min_dependents: int) -> None:
    """Analyze codebase to identify shared code components."""
    click.echo(f"Analyzing {directory}...")

    # Find all Python files
    python_files = find_python_files(directory)
    click.echo(f"Found {len(python_files)} Python files")

    # Analyze each file
    analyses = []
    for file_path in python_files:
        analysis = analyze_file(file_path)
        analyses.append(analysis)

    click.echo(f"Analyzed {len(analyses)} files")

    # Build dependency graph
    graph = build_dependency_graph(analyses)
    click.echo(f"Built dependency graph with {len(graph)} modules")

    # Find shared components
    shared = find_shared_components(graph, min_dependents)
    click.echo(f"Found {len(shared)} shared components (used by {min_dependents}+ modules)")

    # Categorize components
    categorized = defaultdict(list)
    for module_path, data in shared.items():
        category = categorize_component(module_path)
        categorized[category].append({
            "module": module_path,
            "dependent_count": data["dependent_count"],
            "dependents": data["dependents"][:10],  # Limit to first 10
            "lines": data["lines"],
        })

    # Prepare output
    result = {
        "summary": {
            "total_files": len(analyses),
            "total_modules": len(graph),
            "shared_components": len(shared),
            "min_dependents": min_dependents,
        },
        "shared_components_by_category": {
            category: sorted(components, key=lambda x: x["dependent_count"], reverse=True)
            for category, components in categorized.items()
        },
        "all_shared_components": {
            module: {
                "dependent_count": data["dependent_count"],
                "dependents": data["dependents"],
                "lines": data["lines"],
                "category": categorize_component(module),
            }
            for module, data in shared.items()
        },
    }

    # Write output
    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    click.echo(f"\nResults written to {output}")
    click.echo("\nSummary by category:")
    for category, components in categorized.items():
        click.echo(f"  {category}: {len(components)} components")
        for comp in sorted(components, key=lambda x: x["dependent_count"], reverse=True)[:5]:
            click.echo(f"    - {comp['module']} ({comp['dependent_count']} dependents)")


if __name__ == "__main__":
    main()
