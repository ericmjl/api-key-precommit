from pathlib import Path
import tempfile
import yaml
import re

import pytest

from api_key_checker.checker import APIKeyChecker


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        yield Path(f.name)
    Path(f.name).unlink()


@pytest.fixture
def config_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(
            """
patterns:
  - '[A-Z0-9]{32}'
  - 'sk-[A-Za-z0-9]{48}'
"""
        )
        yield Path(f.name)
    Path(f.name).unlink()


def test_default_pattern(temp_file):
    content = "Here's an API key: abcd1234efgh5678ijkl9012mnop3456"
    temp_file.write_text(content)

    checker = APIKeyChecker()
    violations = checker.check_file(temp_file)

    assert len(violations) == 1
    assert "abcd1234efgh5678ijkl9012mnop3456" in violations[0]


def test_custom_patterns(temp_file):
    checker = APIKeyChecker(patterns=[r"sk-[A-Za-z0-9]{48}"])

    content = "OpenAI key: sk-abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx"
    temp_file.write_text(content)

    violations = checker.check_file(temp_file)
    assert len(violations) == 1


def test_config_file(temp_file, config_file):
    checker = APIKeyChecker(config_path=config_file)

    content = """
    API key 1: ABCD1234EFGH5678IJKL9012MNOP3456
    API key 2: sk-abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx
    """
    temp_file.write_text(content)

    violations = checker.check_file(temp_file)
    assert len(violations) == 2


def test_binary_file(temp_file):
    # Write some binary content
    with open(temp_file, "wb") as f:
        f.write(b"\x00\x01\x02\x03")

    checker = APIKeyChecker()
    violations = checker.check_file(temp_file)

    assert len(violations) == 0


def test_pattern_strings():
    checker = APIKeyChecker(patterns=[])
    yaml_patterns = """
    patterns:
      - '[A-Z0-9]{32}'
      - 'sk-[A-Za-z0-9]{48}'
    """
    parsed = yaml.safe_load(yaml_patterns)
    if isinstance(parsed, dict) and "patterns" in parsed:
        checker.patterns.update({p: re.compile(p) for p in parsed["patterns"]})

    content = """
    API key 1: ABCD1234EFGH5678IJKL9012MNOP3456
    API key 2: sk-abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(content)
        temp_file = Path(f.name)

    try:
        violations = checker.check_file(temp_file)
        assert len(violations) == 2
    finally:
        temp_file.unlink()
