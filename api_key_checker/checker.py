from pathlib import Path
from typing import List, Dict, Pattern
import re

import typer
from loguru import logger

app = typer.Typer()


@app.command()
def main(
    files: List[Path] = typer.Argument(
        ...,
        help="Files to check",
        # This tells typer to collect all positional arguments until --patterns
    ),
    patterns: List[str] = typer.Option(
        None,
        "--pattern",
        "-p",
        help="Regex patterns to check for API keys. Can be specified multiple times.",
    ),
) -> int:
    """Check files for exposed API keys."""
    # Compile patterns
    if not patterns:
        # Default pattern matches common API key formats
        default_pattern = r"[a-zA-Z0-9]{32,}"
        compiled_patterns: Dict[str, Pattern] = {
            default_pattern: re.compile(default_pattern)
        }
    else:
        compiled_patterns = {pattern: re.compile(pattern) for pattern in patterns}

    has_violations = False
    for file in files:
        print(file)
        if not file.is_file():
            continue

        # Check file content
        try:
            content = file.read_text()
        except UnicodeDecodeError:
            logger.warning(f"Skipping binary file: {file}")
            continue

        # Look for matches
        for pattern_str, pattern in compiled_patterns.items():
            logger.info(f"Checking pattern: {pattern_str}")
            matches = pattern.finditer(content)
            for match in matches:
                has_violations = True
                error = (
                    f"Found potential API key matching pattern '{pattern_str}' "
                    f"in {file}:{match.start()}-{match.end()}"
                )
                raise Exception(error)


if __name__ == "__main__":
    app()
