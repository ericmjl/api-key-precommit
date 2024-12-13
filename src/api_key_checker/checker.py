from pathlib import Path
from typing import List, Optional, Dict, Pattern
import re

import typer
import yaml
from loguru import logger

app = typer.Typer()


class APIKeyChecker:
    """Check files for exposed API keys using configurable regex patterns.

    :param patterns: List of regex patterns to check for
    :param config_path: Path to YAML config file with patterns
    """

    def __init__(
        self, patterns: Optional[List[str]] = None, config_path: Optional[Path] = None
    ) -> None:
        self.patterns: Dict[str, Pattern] = {}

        if config_path:
            self._load_config(config_path)
        if patterns:
            self.patterns.update({pattern: re.compile(pattern) for pattern in patterns})

        if not self.patterns:
            # Default pattern matches common API key formats
            default_pattern = r"[a-zA-Z0-9]{32,}"
            self.patterns = {default_pattern: re.compile(default_pattern)}

    def _load_config(self, config_path: Path) -> None:
        """Load patterns from YAML config file.

        :param config_path: Path to YAML config file
        """
        with open(config_path) as f:
            config = yaml.safe_load(f)

        patterns = config.get("patterns", [])
        self.patterns.update({pattern: re.compile(pattern) for pattern in patterns})

    def check_file(self, file_path: Path) -> List[str]:
        """Check a single file for API key patterns.

        :param file_path: Path to file to check
        :returns: List of found API keys
        """
        violations = []

        try:
            content = file_path.read_text()
        except UnicodeDecodeError:
            logger.warning(f"Skipping binary file: {file_path}")
            return violations

        for pattern_str, pattern in self.patterns.items():
            matches = pattern.finditer(content)
            for match in matches:
                violations.append(
                    f"Found potential API key matching pattern '{pattern_str}' "
                    f"in {file_path}:{match.start()}-{match.end()}"
                )

        return violations


@app.command()
def main(
    files: List[Path] = typer.Argument(..., help="Files to check"),
    config: Optional[Path] = typer.Option(
        None, help="Path to YAML config file with patterns"
    ),
    patterns: Optional[List[str]] = typer.Option(
        None, help="Additional regex patterns to check"
    ),
    pattern_strings: Optional[str] = typer.Option(
        None, help="YAML-formatted patterns string from pre-commit config"
    ),
) -> int:
    """Check files for exposed API keys."""
    # Parse pattern_strings if provided
    extra_patterns = []
    if pattern_strings:
        try:
            parsed_patterns = yaml.safe_load(pattern_strings)
            if isinstance(parsed_patterns, list):
                extra_patterns.extend(parsed_patterns)
            elif isinstance(parsed_patterns, dict) and "patterns" in parsed_patterns:
                extra_patterns.extend(parsed_patterns["patterns"])
        except yaml.YAMLError:
            logger.error("Failed to parse pattern_strings as YAML")

    if patterns:
        extra_patterns.extend(patterns)

    checker = APIKeyChecker(patterns=extra_patterns, config_path=config)

    has_violations = False
    for file_path in files:
        if not file_path.is_file():
            continue

        violations = checker.check_file(file_path)
        if violations:
            has_violations = True
            for violation in violations:
                logger.error(violation)

    return 1 if has_violations else 0


if __name__ == "__main__":
    app()
