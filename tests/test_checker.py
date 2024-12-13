from pathlib import Path
import pytest
from api_key_checker.checker import APIKeyChecker

@pytest.fixture
def checker():
    return APIKeyChecker()

def test_check_file_with_api_key(tmp_path, checker):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Here's a key: sk-proj-1234-abcd")

    assert checker.check_file(test_file) is True

def test_check_file_without_api_key(tmp_path, checker):
    test_file = tmp_path / "test.txt"
    test_file.write_text("No API keys here")

    assert checker.check_file(test_file) is False

def test_check_binary_file(tmp_path, checker):
    test_file = tmp_path / "test.bin"
    test_file.write_bytes(b'\x00\x01\x02\x03')

    assert checker.check_file(test_file) is False
